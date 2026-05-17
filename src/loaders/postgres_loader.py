"""
PostgreSQL data loader.
Handles insert/update operations for all tables.
"""
from typing import List, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from src.config.settings import DATABASE_URL
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PostgresLoader:
    """PostgreSQL data loader with batch operations."""

    def __init__(self):
        self.engine = create_engine(DATABASE_URL, poolclass=NullPool)

    def insert_raw_gsc(self, data: List[Dict[str, Any]]):
        """Insert raw GSC data with upsert."""
        if not data:
            return

        query = text("""
            INSERT INTO raw_gsc_queries (date, query, page, clicks, impressions, ctr, position, site)
            VALUES (:date, :query, :page, :clicks, :impressions, :ctr, :position, :site)
            ON CONFLICT (date, query, page, site) DO UPDATE SET
                clicks = EXCLUDED.clicks,
                impressions = EXCLUDED.impressions,
                ctr = EXCLUDED.ctr,
                position = EXCLUDED.position
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} GSC rows")

    def insert_raw_ga4(self, data: List[Dict[str, Any]]):
        """Insert raw GA4 data with upsert."""
        if not data:
            return

        query = text("""
            INSERT INTO raw_ga4_sessions (date, page, sessions, users, revenue, source_medium)
            VALUES (:date, :page, :sessions, :users, :revenue, :source_medium)
            ON CONFLICT (date, page, source_medium) DO UPDATE SET
                sessions = EXCLUDED.sessions,
                users = EXCLUDED.users,
                revenue = EXCLUDED.revenue
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} GA4 rows")

    def insert_raw_ym(self, data: List[Dict[str, Any]]):
        """Insert raw Yandex Metrika data with upsert."""
        if not data:
            return

        query = text("""
            INSERT INTO raw_ym_traffic (date, page, visits, users, bounce_rate, source, search_phrase)
            VALUES (:date, :page, :visits, :users, :bounce_rate, :source, :search_phrase)
            ON CONFLICT (date, page, source, search_phrase) DO UPDATE SET
                visits = EXCLUDED.visits,
                users = EXCLUDED.users,
                bounce_rate = EXCLUDED.bounce_rate
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} Y.Metrika rows")

    def insert_raw_yw(self, data: List[Dict[str, Any]]):
        """Insert raw Yandex Webmaster problems."""
        if not data:
            return

        query = text("""
            INSERT INTO raw_yw_problems (date, host_id, problem_type, url, severity, message)
            VALUES (:date, :host_id, :problem_type, :url, :severity, :message)
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} Y.Webmaster rows")

    def insert_clusters(self, data: List[Dict[str, Any]]):
        """Insert or update cluster mappings."""
        if not data:
            return

        query = text("""
            INSERT INTO clusters (page, cluster_name, category, subcategory, priority, notes)
            VALUES (:page, :cluster_name, :category, :subcategory, :priority, :notes)
            ON CONFLICT (page) DO UPDATE SET
                cluster_name = EXCLUDED.cluster_name,
                category = EXCLUDED.category,
                subcategory = EXCLUDED.subcategory,
                priority = EXCLUDED.priority,
                notes = EXCLUDED.notes,
                updated_at = CURRENT_TIMESTAMP
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} cluster mappings")

    def insert_processed_traffic(self, data: List[Dict[str, Any]]):
        """Insert processed traffic data."""
        if not data:
            return

        query = text("""
            INSERT INTO processed_traffic (date, page, cluster_name, category, sessions, users, revenue, source)
            VALUES (:date, :page, :cluster_name, :category, :sessions, :users, :revenue, :source)
            ON CONFLICT (date, page, source) DO UPDATE SET
                sessions = EXCLUDED.sessions,
                users = EXCLUDED.users,
                revenue = EXCLUDED.revenue
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} processed traffic rows")

    def insert_processed_positions(self, data: List[Dict[str, Any]]):
        """Insert processed positions data."""
        if not data:
            return

        query = text("""
            INSERT INTO processed_positions (date, query, page, cluster_name, position, impressions, clicks, ctr, search_engine)
            VALUES (:date, :query, :page, :cluster_name, :position, :impressions, :clicks, :ctr, :search_engine)
            ON CONFLICT (date, query, page, search_engine) DO UPDATE SET
                position = EXCLUDED.position,
                impressions = EXCLUDED.impressions,
                clicks = EXCLUDED.clicks,
                ctr = EXCLUDED.ctr
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} processed positions rows")

    def insert_processed_visibility(self, data: List[Dict[str, Any]]):
        """Insert processed visibility data."""
        if not data:
            return

        query = text("""
            INSERT INTO processed_visibility (date, cluster_name, category, visibility_score, search_engine)
            VALUES (:date, :cluster_name, :category, :visibility_score, :search_engine)
            ON CONFLICT (date, cluster_name, category, search_engine) DO UPDATE SET
                visibility_score = EXCLUDED.visibility_score
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} visibility rows")

    def insert_alerts(self, data: List[Dict[str, Any]]):
        """Insert alerts."""
        if not data:
            return

        query = text("""
            INSERT INTO alerts (alert_date, alert_type, severity, message, metric_value, threshold, page, query, cluster_name)
            VALUES (:alert_date, :alert_type, :severity, :message, :metric_value, :threshold, :page, :query, :cluster_name)
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} alerts")

    def insert_weekly_tops(self, data: List[Dict[str, Any]]):
        """Insert weekly top data."""
        if not data:
            return

        query = text("""
            INSERT INTO weekly_tops (date, category, page, cluster_name, metric_name, metric_value, rank, trend, change_value)
            VALUES (:date, :category, :page, :cluster_name, :metric_name, :metric_value, :rank, :trend, :change_value)
        """)

        with self.engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()

        logger.info(f"Loaded {len(data)} top rows")

    def execute_query(self, query: str, params: dict = None) -> List[Dict]:
        """Execute raw SQL query and return results."""
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row._mapping) for row in result]


if __name__ == '__main__':
    loader = PostgresLoader()
    print("PostgresLoader initialized")
