from datetime import datetime
"""
Yandex Webmaster API Client.
Extracts: indexing errors, critical problems.
"""
from typing import List, Dict, Any
import requests
from src.config.settings import YANDEX_WEBMASTER_TOKEN, YANDEX_WEBMASTER_HOST_ID
from src.utils.logger import get_logger

logger = get_logger(__name__)

class YandexWebmasterClient:
    """Yandex Webmaster API client."""

    BASE_URL = "https://api.webmaster.yandex.net/v4"

    def __init__(self):
        self.token = YANDEX_WEBMASTER_TOKEN
        self.host_id = YANDEX_WEBMASTER_HOST_ID
        self.headers = {
            'Authorization': f'OAuth {self.token}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint: str) -> Dict:
        """Make API request with error handling."""
        url = f"{self.BASE_URL}/user/{self._get_user_id()}/hosts/{self.host_id}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Yandex Webmaster API error: {e}")
            raise

    def _get_user_id(self) -> str:
        """Get user ID from API."""
        try:
            response = requests.get(
                f"{self.BASE_URL}/user",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get('user_id', '')
        except Exception as e:
            logger.error(f"Failed to get user ID: {e}")
            raise

    def get_indexing_problems(self) -> List[Dict[str, Any]]:
        """
        Fetch indexing problems from Yandex Webmaster.

        Returns:
            List of problems with type, url, severity, message
        """
        try:
            data = self._make_request("/indexing/problems")

            rows = []
            for problem in data.get('problems', []):
                rows.append({
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'host_id': self.host_id,
                    'problem_type': problem.get('type', 'unknown'),
                    'url': problem.get('url', ''),
                    'severity': problem.get('severity', 'warning'),
                    'message': problem.get('message', '')
                })

            logger.info(f"Y.Webmaster: Fetched {len(rows)} problems")
            return rows

        except Exception as e:
            logger.warning(f"Y.Webmaster problems fetch failed: {e}")
            return []

    def get_critical_errors(self) -> List[Dict[str, Any]]:
        """Get only critical errors."""
        all_problems = self.get_indexing_problems()
        critical = [p for p in all_problems if p.get('severity') == 'critical']
        logger.info(f"Y.Webmaster: {len(critical)} critical errors found")
        return critical


if __name__ == '__main__':
    from datetime import datetime
    client = YandexWebmasterClient()
    problems = client.get_indexing_problems()
    print(f"Test fetch: {len(problems)} problems")
