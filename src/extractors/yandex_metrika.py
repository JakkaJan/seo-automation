"""
Yandex Metrika API Client.
Extracts: visits, users, bounce rate, search phrases.
"""
from typing import List, Dict, Any
import requests
from src.config.settings import YANDEX_METRIKA_TOKEN, YANDEX_METRIKA_COUNTER_ID
from src.utils.logger import get_logger

logger = get_logger(__name__)

class YandexMetrikaClient:
    """Yandex Metrika API client."""

    BASE_URL = "https://api-metrika.yandex.net/stat/v1/data"

    def __init__(self):
        self.token = YANDEX_METRIKA_TOKEN
        self.counter_id = YANDEX_METRIKA_COUNTER_ID
        self.headers = {
            'Authorization': f'OAuth {self.token}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, params: Dict) -> Dict:
        """Make API request with error handling."""
        try:
            response = requests.get(self.BASE_URL, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Yandex Metrika API error: {e}")
            raise

    def get_traffic_by_page(
        self,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Fetch traffic data by page.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of rows with page, visits, users, bounce_rate
        """
        params = {
            'ids': self.counter_id,
            'date1': start_date,
            'date2': end_date,
            'metrics': 'ym:s:visits,ym:s:users,ym:s:bounceRate',
            'dimensions': 'ym:pv:URLPath',
            'limit': 10000,
            'accuracy': 'full'
        }

        data = self._make_request(params)

        rows = []
        for item in data.get('data', []):
            dimensions = item.get('dimensions', [])
            metrics = item.get('metrics', [])

            rows.append({
                'date': start_date,
                'page': dimensions[0].get('name', '') if dimensions else '',
                'visits': int(metrics[0]) if len(metrics) > 0 else 0,
                'users': int(metrics[1]) if len(metrics) > 1 else 0,
                'bounce_rate': round(float(metrics[2]), 2) if len(metrics) > 2 else 0,
                'source': 'yandex'
            })

        logger.info(f"Y.Metrika: Fetched {len(rows)} rows for {start_date} to {end_date}")
        return rows

    def get_search_phrases(
        self,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Fetch search phrases that brought traffic.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of rows with search_phrase, page, visits
        """
        params = {
            'ids': self.counter_id,
            'date1': start_date,
            'date2': end_date,
            'metrics': 'ym:s:visits',
            'dimensions': 'ym:s:searchPhrase,ym:pv:URLPath',
            'limit': 10000,
            'filters': "ym:s:trafficSource=='organic'"
        }

        data = self._make_request(params)

        rows = []
        for item in data.get('data', []):
            dimensions = item.get('dimensions', [])
            metrics = item.get('metrics', [])

            rows.append({
                'date': start_date,
                'page': dimensions[1].get('name', '') if len(dimensions) > 1 else '',
                'visits': int(metrics[0]) if metrics else 0,
                'search_phrase': dimensions[0].get('name', '') if dimensions else '',
                'source': 'yandex'
            })

        logger.info(f"Y.Metrika: Fetched {len(rows)} search phrases")
        return rows


if __name__ == '__main__':
    from datetime import datetime, timedelta
    client = YandexMetrikaClient()
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    data = client.get_traffic_by_page(start, end)
    print(f"Test fetch: {len(data)} rows")
