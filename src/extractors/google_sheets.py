"""
Google Sheets integration for cluster data.
"""
from typing import List, Dict, Any
import gspread
from google.oauth2.service_account import Credentials
from src.config.settings import GOOGLE_SERVICE_ACCOUNT_KEY, GOOGLE_SHEETS_URL
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GoogleSheetsClient:
    """Google Sheets client for cluster data."""

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]

    def __init__(self):
        self.client = None
        self.sheet_url = GOOGLE_SHEETS_URL
        self._authenticate()

    def _authenticate(self):
        """Authenticate with service account."""
        try:
            credentials = Credentials.from_service_account_file(
                GOOGLE_SERVICE_ACCOUNT_KEY,
                scopes=self.SCOPES
            )
            self.client = gspread.authorize(credentials)
            logger.info("Google Sheets authentication successful")
        except Exception as e:
            logger.error(f"Google Sheets authentication failed: {e}")
            raise

    def get_clusters(self, worksheet_name: str = "Clusters") -> List[Dict[str, Any]]:
        """
        Fetch cluster mapping from Google Sheets.

        Expected columns: URL, Cluster_Name, Category, Subcategory, Priority, Notes

        Returns:
            List of cluster dictionaries
        """
        try:
            spreadsheet = self.client.open_by_url(self.sheet_url)
            worksheet = spreadsheet.worksheet(worksheet_name)

            # Get all records
            records = worksheet.get_all_records()

            clusters = []
            for record in records:
                clusters.append({
                    'page': record.get('URL', '').strip(),
                    'cluster_name': record.get('Cluster_Name', 'Без кластера').strip(),
                    'category': record.get('Category', '').strip(),
                    'subcategory': record.get('Subcategory', '').strip(),
                    'priority': record.get('Priority', 'Medium').strip(),
                    'notes': record.get('Notes', '').strip()
                })

            logger.info(f"Sheets: Fetched {len(clusters)} cluster mappings")
            return clusters

        except Exception as e:
            logger.error(f"Google Sheets fetch error: {e}")
            raise

    def update_report_sheet(self, data: List[Dict], worksheet_name: str = "SEO_Report"):
        """Update report sheet with processed data."""
        try:
            spreadsheet = self.client.open_by_url(self.sheet_url)

            # Try to get worksheet, create if not exists
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
                worksheet.clear()
            except gspread.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(worksheet_name, rows=1000, cols=20)

            # Prepare headers and data
            if not data:
                logger.warning("No data to write to sheet")
                return

            headers = list(data[0].keys())
            rows = [headers]
            for item in data:
                rows.append([str(item.get(h, '')) for h in headers])

            worksheet.update(rows)
            logger.info(f"Sheets: Updated {worksheet_name} with {len(data)} rows")

        except Exception as e:
            logger.error(f"Google Sheets update error: {e}")
            raise


if __name__ == '__main__':
    client = GoogleSheetsClient()
    clusters = client.get_clusters()
    print(f"Test fetch: {len(clusters)} clusters")
    if clusters:
        print(f"Sample: {clusters[0]}")
