"""
Google Analytics 4 API Client.
Extracts: sessions, users, revenue by page.
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, FilterExpression, Filter
)
from google.oauth2 import service_account
from src.config.settings import GOOGLE_SERVICE_ACCOUNT_KEY, GA4_PROPERTY_ID
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GA4Client:
    """Google Analytics 4 Data API client."""

    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

    def __init__(self):
        self.client = None
        self.property_id = GA4_PROPERTY_ID
        self._authenticate()

    def _authenticate(self):
        """Authenticate with service account."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_SERVICE_ACCOUNT_KEY,
                scopes=self.SCOPES
            )
            self.client = BetaAnalyticsDataClient(credentials=credentials)
            logger.info("GA4 authentication successful")
        except Exception as e:
            logger.error(f"GA4 authentication failed: {e}")
            raise

    def get_sessions_by_page(
        self,
        start_date: str,
        end_date: str,
        source_filter: str = 'organic'
    ) -> List[Dict[str, Any]]:
        """
        Fetch sessions, users, revenue by page.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            source_filter: Filter by session source (default: organic)

        Returns:
            List of rows with page, sessions, users, revenue
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[
                Dimension(name="pagePath"),
                Dimension(name="sessionSource")
            ],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="purchaseRevenue")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
        )

        try:
            response = self.client.run_report(request)

            rows = []
            for row in response.rows:
                page = row.dimension_values[0].value
                source = row.dimension_values[1].value

                # Filter for organic traffic
                if source_filter and source_filter.lower() not in source.lower():
                    continue

                rows.append({
                    'date': start_date,
                    'page': page,
                    'sessions': int(row.metric_values[0].value or 0),
                    'users': int(row.metric_values[1].value or 0),
                    'revenue': float(row.metric_values[2].value or 0),
                    'source_medium': f"{source} / organic"
                })

            logger.info(f"GA4: Fetched {len(rows)} rows for {start_date} to {end_date}")
            return rows

        except Exception as e:
            logger.error(f"GA4 API error: {e}")
            raise


if __name__ == '__main__':
    # Test connection
    client = GA4Client()
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    data = client.get_sessions_by_page(start, end)
    print(f"Test fetch: {len(data)} rows")
