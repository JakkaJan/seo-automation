"""
Tests for data extractors.
"""
import pytest
from unittest.mock import Mock, patch
from src.extractors.gsc_client import GSCClient
from src.extractors.ga4_client import GA4Client

class TestGSCClient:
    """Tests for Google Search Console client."""

    @patch('src.extractors.gsc_client.build')
    @patch('src.extractors.gsc_client.service_account.Credentials')
    def test_authenticate(self, mock_creds, mock_build):
        """Test GSC authentication."""
        mock_creds.from_service_account_file.return_value = Mock()
        mock_build.return_value = Mock()

        client = GSCClient()
        assert client.service is not None

    @patch('src.extractors.gsc_client.build')
    @patch('src.extractors.gsc_client.service_account.Credentials')
    def test_get_search_analytics(self, mock_creds, mock_build):
        """Test search analytics fetch."""
        mock_service = Mock()
        mock_response = {
            'rows': [
                {
                    'keys': ['test query', '/page1'],
                    'clicks': 100,
                    'impressions': 1000,
                    'ctr': 0.1,
                    'position': 5.5
                }
            ]
        }
        mock_service.searchanalytics().query().execute.return_value = mock_response
        mock_build.return_value = mock_service

        client = GSCClient()
        data = client.get_search_analytics('2026-01-01', '2026-01-07')

        assert len(data) == 1
        assert data[0]['query'] == 'test query'
        assert data[0]['clicks'] == 100

class TestGA4Client:
    """Tests for Google Analytics 4 client."""

    @patch('src.extractors.ga4_client.BetaAnalyticsDataClient')
    @patch('src.extractors.ga4_client.service_account.Credentials')
    def test_authenticate(self, mock_creds, mock_client):
        """Test GA4 authentication."""
        mock_creds.from_service_account_file.return_value = Mock()
        mock_client.return_value = Mock()

        client = GA4Client()
        assert client.client is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
