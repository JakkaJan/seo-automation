"""
Alert engine for SEO anomalies.
Simple rule-based alerts for MVP.
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
from src.config.settings import (
    ALERT_TRAFFIC_DROP_PCT,
    ALERT_POSITION_DROP_POINTS,
    ALERT_POSITION_MIN_IMPRESSIONS,
    ALERT_CTR_DROP_PCT
)
from src.loaders.postgres_loader import PostgresLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AlertEngine:
    """Rule-based alert engine for SEO monitoring."""

    def __init__(self):
        self.loader = PostgresLoader()

    def check_traffic_drops(self, current_date: str, previous_date: str) -> List[Dict]:
        """Check for traffic drops by cluster/category."""
        query = """
            WITH current_week AS (
                SELECT cluster_name, category, SUM(sessions) as sessions
                FROM processed_traffic
                WHERE date = :current_date AND source = 'google'
                GROUP BY cluster_name, category
            ),
            previous_week AS (
                SELECT cluster_name, category, SUM(sessions) as sessions
                FROM processed_traffic
                WHERE date = :previous_date AND source = 'google'
                GROUP BY cluster_name, category
            )
            SELECT 
                COALESCE(c.cluster_name, p.cluster_name) as cluster_name,
                COALESCE(c.category, p.category) as category,
                COALESCE(c.sessions, 0) as current_sessions,
                COALESCE(p.sessions, 0) as previous_sessions
            FROM current_week c
            FULL OUTER JOIN previous_week p 
                ON c.cluster_name = p.cluster_name AND c.category = p.category
            WHERE COALESCE(p.sessions, 0) > 0
        """

        results = self.loader.execute_query(query, {
            'current_date': current_date,
            'previous_date': previous_date
        })

        alerts = []
        for row in results:
            prev = row['previous_sessions'] or 1  # Avoid division by zero
            curr = row['current_sessions'] or 0
            drop_pct = ((prev - curr) / prev) * 100

            if drop_pct >= ALERT_TRAFFIC_DROP_PCT:
                alerts.append({
                    'alert_date': current_date,
                    'alert_type': 'traffic_drop',
                    'severity': 'critical' if drop_pct >= 30 else 'warning',
                    'message': f"Traffic dropped {drop_pct:.1f}% for cluster '{row['cluster_name']}'",
                    'metric_value': curr,
                    'threshold': prev * (1 - ALERT_TRAFFIC_DROP_PCT / 100),
                    'page': None,
                    'query': None,
                    'cluster_name': row['cluster_name']
                })

        logger.info(f"Traffic drop alerts: {len(alerts)}")
        return alerts

    def check_position_drops(self, current_date: str, previous_date: str) -> List[Dict]:
        """Check for position drops on high-traffic keywords."""
        query = """
            WITH current_week AS (
                SELECT query, page, cluster_name, position, impressions
                FROM processed_positions
                WHERE date = :current_date AND search_engine = 'google'
            ),
            previous_week AS (
                SELECT query, page, cluster_name, position, impressions
                FROM processed_positions
                WHERE date = :previous_date AND search_engine = 'google'
            )
            SELECT 
                COALESCE(c.query, p.query) as query,
                COALESCE(c.page, p.page) as page,
                COALESCE(c.cluster_name, p.cluster_name) as cluster_name,
                COALESCE(c.position, 0) as current_position,
                COALESCE(p.position, 0) as previous_position,
                COALESCE(c.impressions, p.impressions, 0) as impressions
            FROM current_week c
            FULL OUTER JOIN previous_week p 
                ON c.query = p.query AND c.page = p.page
            WHERE COALESCE(p.position, 0) > 0
        """

        results = self.loader.execute_query(query, {
            'current_date': current_date,
            'previous_date': previous_date
        })

        alerts = []
        for row in results:
            if row['impressions'] < ALERT_POSITION_MIN_IMPRESSIONS:
                continue

            prev_pos = row['previous_position']
            curr_pos = row['current_position']

            if curr_pos == 0 or prev_pos == 0:
                continue

            drop = curr_pos - prev_pos

            if drop >= ALERT_POSITION_DROP_POINTS:
                alerts.append({
                    'alert_date': current_date,
                    'alert_type': 'position_drop',
                    'severity': 'critical' if drop >= 15 else 'warning',
                    'message': f"Position dropped {drop:.0f} points for '{row['query']}' (now {curr_pos:.1f})",
                    'metric_value': curr_pos,
                    'threshold': prev_pos + ALERT_POSITION_DROP_POINTS,
                    'page': row['page'],
                    'query': row['query'],
                    'cluster_name': row['cluster_name']
                })

        logger.info(f"Position drop alerts: {len(alerts)}")
        return alerts

    def check_ctr_drops(self, current_date: str, previous_date: str) -> List[Dict]:
        """Check for CTR drops."""
        query = """
            WITH current_week AS (
                SELECT query, page, cluster_name, ctr
                FROM processed_positions
                WHERE date = :current_date AND search_engine = 'google'
            ),
            previous_week AS (
                SELECT query, page, cluster_name, ctr
                FROM processed_positions
                WHERE date = :previous_date AND search_engine = 'google'
            )
            SELECT 
                COALESCE(c.query, p.query) as query,
                COALESCE(c.page, p.page) as page,
                COALESCE(c.cluster_name, p.cluster_name) as cluster_name,
                COALESCE(c.ctr, 0) as current_ctr,
                COALESCE(p.ctr, 0) as previous_ctr
            FROM current_week c
            FULL OUTER JOIN previous_week p 
                ON c.query = p.query AND c.page = p.page
            WHERE COALESCE(p.ctr, 0) > 0
        """

        results = self.loader.execute_query(query, {
            'current_date': current_date,
            'previous_date': previous_date
        })

        alerts = []
        for row in results:
            prev_ctr = row['previous_ctr']
            curr_ctr = row['current_ctr']

            if prev_ctr == 0 or curr_ctr == 0:
                continue

            drop_pct = ((prev_ctr - curr_ctr) / prev_ctr) * 100

            if drop_pct >= ALERT_CTR_DROP_PCT:
                alerts.append({
                    'alert_date': current_date,
                    'alert_type': 'ctr_drop',
                    'severity': 'warning',
                    'message': f"CTR dropped {drop_pct:.1f}% for '{row['query']}'",
                    'metric_value': curr_ctr,
                    'threshold': prev_ctr * (1 - ALERT_CTR_DROP_PCT / 100),
                    'page': row['page'],
                    'query': row['query'],
                    'cluster_name': row['cluster_name']
                })

        logger.info(f"CTR drop alerts: {len(alerts)}")
        return alerts

    def check_crawl_errors(self, current_date: str) -> List[Dict]:
        """Check for new crawl errors from GSC."""
        query = """
            SELECT problem_type, url, severity, message
            FROM raw_yw_problems
            WHERE date = :current_date AND severity = 'critical'
        """

        results = self.loader.execute_query(query, {'current_date': current_date})

        alerts = []
        for row in results:
            alerts.append({
                'alert_date': current_date,
                'alert_type': 'crawl_error',
                'severity': 'critical',
                'message': f"Crawl error: {row['problem_type']} on {row['url']}",
                'metric_value': None,
                'threshold': None,
                'page': row['url'],
                'query': None,
                'cluster_name': None
            })

        logger.info(f"Crawl error alerts: {len(alerts)}")
        return alerts

    def run_all_checks(self, current_date: str, previous_date: str) -> List[Dict]:
        """Run all alert checks and return combined results."""
        all_alerts = []

        all_alerts.extend(self.check_traffic_drops(current_date, previous_date))
        all_alerts.extend(self.check_position_drops(current_date, previous_date))
        all_alerts.extend(self.check_ctr_drops(current_date, previous_date))
        all_alerts.extend(self.check_crawl_errors(current_date))

        # Save to database
        if all_alerts:
            self.loader.insert_alerts(all_alerts)

        logger.info(f"Total alerts generated: {len(all_alerts)}")
        return all_alerts


if __name__ == '__main__':
    engine = AlertEngine()
    print("AlertEngine initialized")
