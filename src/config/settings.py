"""
Application settings loaded from environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# =============================================================================
# DATABASE
# =============================================================================
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://airflow:airflow@postgres:5432/airflow')

# =============================================================================
# GOOGLE APIs
# =============================================================================
GOOGLE_SERVICE_ACCOUNT_KEY = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY', '')
GSC_SITE_URL = os.getenv('GSC_SITE_URL', '')
GA4_PROPERTY_ID = os.getenv('GA4_PROPERTY_ID', '')
GOOGLE_SHEETS_URL = os.getenv('GOOGLE_SHEETS_URL', '')

# =============================================================================
# YANDEX APIs
# =============================================================================
YANDEX_METRIKA_TOKEN = os.getenv('YANDEX_METRIKA_TOKEN', '')
YANDEX_METRIKA_COUNTER_ID = os.getenv('YANDEX_METRIKA_COUNTER_ID', '')
YANDEX_WEBMASTER_TOKEN = os.getenv('YANDEX_WEBMASTER_TOKEN', '')
YANDEX_WEBMASTER_HOST_ID = os.getenv('YANDEX_WEBMASTER_HOST_ID', '')

# =============================================================================
# TELEGRAM
# =============================================================================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# =============================================================================
# EMAIL (SendGrid)
# =============================================================================
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
EMAIL_FROM = os.getenv('EMAIL_FROM', '')
EMAIL_TO = os.getenv('EMAIL_TO', '').split(',') if os.getenv('EMAIL_TO') else []

# =============================================================================
# VISIBILITY WEIGHTS (adjustable via .env)
# =============================================================================
VISIBILITY_WEIGHTS = {
    'top3': float(os.getenv('VISIBILITY_WEIGHT_TOP3', 1.0)),
    'top10': float(os.getenv('VISIBILITY_WEIGHT_TOP10', 0.5)),
    'top30': float(os.getenv('VISIBILITY_WEIGHT_TOP30', 0.2)),
    'other': float(os.getenv('VISIBILITY_WEIGHT_OTHER', 0.0)),
}

# =============================================================================
# ALERT THRESHOLDS
# =============================================================================
ALERT_TRAFFIC_DROP_PCT = float(os.getenv('ALERT_TRAFFIC_DROP_PCT', 20))
ALERT_POSITION_DROP_POINTS = int(os.getenv('ALERT_POSITION_DROP_POINTS', 8))
ALERT_POSITION_MIN_IMPRESSIONS = int(os.getenv('ALERT_POSITION_MIN_IMPRESSIONS', 500))
ALERT_CTR_DROP_PCT = float(os.getenv('ALERT_CTR_DROP_PCT', 30))

# =============================================================================
# REPORT SETTINGS
# =============================================================================
REPORT_COMPANY_NAME = os.getenv('REPORT_COMPANY_NAME', 'Your Company')
REPORT_LOGO_URL = os.getenv('REPORT_LOGO_URL', '')
REPORT_PRIMARY_COLOR = os.getenv('REPORT_PRIMARY_COLOR', '#2563eb')

# =============================================================================
# PATHS
# =============================================================================
BASE_DIR = Path(__file__).parent.parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'
REPORTS_DIR = BASE_DIR / 'reports'
LOGS_DIR = BASE_DIR / 'logs'

# Create directories if they don't exist
REPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
