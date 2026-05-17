"""
Google Search Console API Client.
Extracts: queries, pages, clicks, impressions, CTR, positions.
"""
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from src.config.settings import GOOGLE_SERVICE_ACCOUNT_KEY, GSC_SITE_URL
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GSCClient:
    """Google Search Console API client."""

    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

    def __init__(self):
        self.service = None
        self.site_url = GSC_SITE_URL
        self._authenticate()

    def _authenticate(self):
        """Authenticate with service account."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_SERVICE_ACCOUNT_KEY,
                scopes=self.SCOPES
            )
            self.service = build('webmasters', 'v3', credentials=credentials)
            logger.info("GSC authentication successful")
        except Exception as e:
            logger.error(f"GSC authentication failed: {e}")
            raise

    def get_search_analytics(
        self,
        start_date: str,
        end_date: str,
        dimensions: List[str] = None,
        row_limit: int = 25000
    ) -> List[Dict[str, Any]]:
        """
        Fetch search analytics data from GSC.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            dimensions: List of dimensions ['query', 'page', 'country', 'device', 'searchAppearance']
            row_limit: Maximum rows to fetch

        Returns:
            List of rows with query, page, clicks, impressions, ctr, position
        """
        if dimensions is None:
            dimensions = ['query', 'page']

        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': row_limit,
            'startRow': 0
        }

        all_rows = []

        try:
            while True:
                response = self.service.searchanalytics().query(
                    siteUrl=self.site_url,
                    body=request_body
                ).execute()

                rows = response.get('rows', [])
                if not rows:
                    break

                for row in rows:
                    keys = row.get('keys', [])
                    all_rows.append({
                        'date': start_date,  # Will be expanded per day in transformer
                        'query': keys[0] if len(keys) > 0 else '',
                        'page': keys[1] if len(keys) > 1 else '',
                        'clicks': row.get('clicks', 0),
                        'impressions': row.get('impressions', 0),
                        'ctr': round(row.get('ctr', 0), 4),
                        'position': round(row.get('position', 0), 2),
                        'site': self.site_url
                    })

                if len(rows) < row_limit:
                    break

                request_body['startRow'] += row_limit

            logger.info(f"GSC: Fetched {len(all_rows)} rows for {start_date} to {end_date}")
            return all_rows

        except Exception as e:
            logger.error(f"GSC API error: {e}")
            raise

    def get_pages(self, start_date: str, end_date: str, row_limit: int = 25000) -> List[Dict]:
        """Fetch page-level analytics (aggregated by page)."""
        return self.get_search_analytics(start_date, end_date, dimensions=['page'], row_limit=row_limit)

    def get_queries(self, start_date: str, end_date: str, row_limit: int = 25000) -> List[Dict]:
        """Fetch query-level analytics (aggregated by query)."""
        return self.get_search_analytics(start_date, end_date, dimensions=['query'], row_limit=row_limit)


if __name__ == '__main__':
    # Test connection
    client = GSCClient()
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    data = client.get_search_analytics(start, end, row_limit=10)
    print(f"Test fetch: {len(data)} rows")
