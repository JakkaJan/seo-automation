"""
Weekly SEO Report DAG.
Runs every Sunday at 8:00 AM.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
import sys
sys.path.insert(0, '/opt/airflow/src')

from src.config.settings import DATABASE_URL
from src.utils.logger import get_logger
from src.utils.date_helpers import get_last_week_range, get_weeks_ago
from src.extractors import GSCClient, GA4Client, YandexMetrikaClient, GoogleSheetsClient
from src.loaders.postgres_loader import PostgresLoader
from src.analytics.alerts import AlertEngine
from src.reporters.pdf_generator import PDFReportGenerator
from src.reporters.telegram_bot import TelegramReporter

logger = get_logger(__name__)

# Default args
default_args = {
    'owner': 'seo-automation',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

# DAG definition
dag = DAG(
    'weekly_seo_report',
    default_args=default_args,
    description='Weekly SEO analytics report generation',
    schedule_interval='0 8 * * 0',  # Sunday 8:00 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['seo', 'reporting'],
)

# =============================================================================
# TASK FUNCTIONS
# =============================================================================

def extract_gsc(**context):
    """Extract Google Search Console data."""
    start_date, end_date = get_last_week_range()
    logger.info(f"Extracting GSC data: {start_date} to {end_date}")

    client = GSCClient()
    data = client.get_search_analytics(start_date, end_date, row_limit=25000)

    loader = PostgresLoader()
    loader.insert_raw_gsc(data)

    context['ti'].xcom_push(key='gsc_rows', value=len(data))
    logger.info(f"GSC extraction complete: {len(data)} rows")
    return f"Extracted {len(data)} GSC rows"

def extract_ga4(**context):
    """Extract Google Analytics 4 data."""
    start_date, end_date = get_last_week_range()
    logger.info(f"Extracting GA4 data: {start_date} to {end_date}")

    client = GA4Client()
    data = client.get_sessions_by_page(start_date, end_date)

    loader = PostgresLoader()
    loader.insert_raw_ga4(data)

    context['ti'].xcom_push(key='ga4_rows', value=len(data))
    logger.info(f"GA4 extraction complete: {len(data)} rows")
    return f"Extracted {len(data)} GA4 rows"

def extract_ym(**context):
    """Extract Yandex Metrika data."""
    start_date, end_date = get_last_week_range()
    logger.info(f"Extracting Y.Metrika data: {start_date} to {end_date}")

    client = YandexMetrikaClient()
    data = client.get_traffic_by_page(start_date, end_date)

    loader = PostgresLoader()
    loader.insert_raw_ym(data)

    context['ti'].xcom_push(key='ym_rows', value=len(data))
    logger.info(f"Y.Metrika extraction complete: {len(data)} rows")
    return f"Extracted {len(data)} Y.Metrika rows"

def extract_clusters(**context):
    """Extract cluster mappings from Google Sheets."""
    logger.info("Extracting cluster data from Google Sheets")

    client = GoogleSheetsClient()
    data = client.get_clusters()

    loader = PostgresLoader()
    loader.insert_clusters(data)

    context['ti'].xcom_push(key='cluster_rows', value=len(data))
    logger.info(f"Cluster extraction complete: {len(data)} rows")
    return f"Extracted {len(data)} cluster mappings"

def transform_data(**context):
    """Transform and aggregate data."""
    start_date, end_date = get_last_week_range()
    logger.info(f"Transforming data for {start_date} to {end_date}")

    loader = PostgresLoader()

    # Aggregate traffic by cluster
    traffic_query = """
        INSERT INTO processed_traffic (date, page, cluster_name, category, sessions, users, revenue, source)
        SELECT 
            r.date,
            r.page,
            c.cluster_name,
            c.category,
            r.sessions,
            r.users,
            r.revenue,
            'google'
        FROM raw_ga4_sessions r
        LEFT JOIN clusters c ON r.page = c.page
        WHERE r.date BETWEEN :start AND :end
        ON CONFLICT (date, page, source) DO UPDATE SET
            sessions = EXCLUDED.sessions,
            users = EXCLUDED.users,
            revenue = EXCLUDED.revenue
    """

    loader.execute_query(traffic_query, {'start': start_date, 'end': end_date})

    # Aggregate positions by cluster
    positions_query = """
        INSERT INTO processed_positions (date, query, page, cluster_name, position, impressions, clicks, ctr, search_engine)
        SELECT 
            r.date,
            r.query,
            r.page,
            c.cluster_name,
            r.position,
            r.impressions,
            r.clicks,
            r.ctr,
            'google'
        FROM raw_gsc_queries r
        LEFT JOIN clusters c ON r.page = c.page
        WHERE r.date BETWEEN :start AND :end
        ON CONFLICT (date, query, page, search_engine) DO UPDATE SET
            position = EXCLUDED.position,
            impressions = EXCLUDED.impressions,
            clicks = EXCLUDED.clicks,
            ctr = EXCLUDED.ctr
    """

    loader.execute_query(positions_query, {'start': start_date, 'end': end_date})

    logger.info("Data transformation complete")
    return "Data transformed successfully"

def generate_alerts(**context):
    """Generate alerts based on rules."""
    current_week_start, _ = get_last_week_range()
    previous_week_start = get_weeks_ago(1, datetime.strptime(current_week_start, '%Y-%m-%d'))

    logger.info(f"Generating alerts: current={current_week_start}, previous={previous_week_start}")

    engine = AlertEngine()
    alerts = engine.run_all_checks(current_week_start, previous_week_start)

    context['ti'].xcom_push(key='alert_count', value=len(alerts))
    logger.info(f"Generated {len(alerts)} alerts")
    return f"Generated {len(alerts)} alerts"

def generate_report(**context):
    """Generate PDF report."""
    start_date, end_date = get_last_week_range()
    logger.info(f"Generating report for {start_date} to {end_date}")

    loader = PostgresLoader()

    # Get summary data
    summary = loader.execute_query("""
        SELECT 
            SUM(sessions) as organic_sessions,
            SUM(revenue) as organic_revenue,
            AVG(position) as avg_position
        FROM processed_traffic
        WHERE date = :date AND source = 'google'
    """, {'date': start_date})

    # Get traffic by cluster
    traffic_data = loader.execute_query("""
        SELECT 
            cluster_name,
            SUM(sessions) as sessions,
            SUM(revenue) as revenue
        FROM processed_traffic
        WHERE date = :date AND source = 'google'
        GROUP BY cluster_name
        ORDER BY sessions DESC
    """, {'date': start_date})

    # Get alerts
    alerts = loader.execute_query("""
        SELECT * FROM alerts 
        WHERE alert_date = :date AND status = 'active'
        ORDER BY severity DESC
    """, {'date': start_date})

    # Get top pages
    tops = loader.execute_query("""
        SELECT page, sessions
        FROM processed_traffic
        WHERE date = :date AND source = 'google'
        ORDER BY sessions DESC
        LIMIT 10
    """, {'date': start_date})

    # Generate PDF
    generator = PDFReportGenerator()
    pdf_path = generator.generate_simple_report(
        start_date,
        {
            'organic_sessions': summary[0].get('organic_sessions', 0) if summary else 0,
            'organic_revenue': summary[0].get('organic_revenue', 0) if summary else 0,
            'avg_position': round(summary[0].get('avg_position', 0), 1) if summary else 0,
        }
    )

    context['ti'].xcom_push(key='pdf_path', value=pdf_path)
    logger.info(f"Report generated: {pdf_path}")
    return f"Report generated: {pdf_path}"

def send_notifications(**context):
    """Send report via Telegram and email."""
    import asyncio

    ti = context['ti']
    pdf_path = ti.xcom_pull(task_ids='generate_report', key='pdf_path')
    alert_count = ti.xcom_pull(task_ids='generate_alerts', key='alert_count')

    logger.info(f"Sending notifications. PDF: {pdf_path}, Alerts: {alert_count}")

    # Send to Telegram
    reporter = TelegramReporter()

    async def send():
        await reporter.send_report(
            pdf_path=pdf_path,
            week_label=get_current_week_label(),
            summary=f"Alerts: {alert_count}"
        )

    asyncio.run(send())

    logger.info("Notifications sent")
    return "Notifications sent successfully"

# =============================================================================
# TASK DEFINITIONS
# =============================================================================

with TaskGroup("extract_data", dag=dag) as extract_group:

    t_extract_gsc = PythonOperator(
        task_id='extract_gsc',
        python_callable=extract_gsc,
        dag=dag,
    )

    t_extract_ga4 = PythonOperator(
        task_id='extract_ga4',
        python_callable=extract_ga4,
        dag=dag,
    )

    t_extract_ym = PythonOperator(
        task_id='extract_ym',
        python_callable=extract_ym,
        dag=dag,
    )

    t_extract_clusters = PythonOperator(
        task_id='extract_clusters',
        python_callable=extract_clusters,
        dag=dag,
    )

t_transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

t_alerts = PythonOperator(
    task_id='generate_alerts',
    python_callable=generate_alerts,
    dag=dag,
)

t_report = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag,
)

t_notify = PythonOperator(
    task_id='send_notifications',
    python_callable=send_notifications,
    dag=dag,
)

# =============================================================================
# DEPENDENCIES
# =============================================================================

extract_group >> t_transform >> t_alerts >> t_report >> t_notify
