import pytest
import requests
import os
import importlib
import external_api
from unittest.mock import Mock, patch
from external_api import get_latest_rates


class TestGetLatestRates:
    @patch.dict(os.environ, {
        'EXCHANGE_RATE_API_URL': 'https://api.exchangerate-api.com/v4/latest',
        'EXTERNAL_API_TIMEOUT': '5'
    })
    @patch('external_api.requests.get')
    def test_successful_request(self, mock_requests_get, sample_rates_response):
        mock_response = Mock()
        mock_response.json.return_value = sample_rates_response
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        rates = get_latest_rates('USD')
        
        assert rates == sample_rates_response['rates']
        mock_requests_get.assert_called_once_with(
            'https://api.exchangerate-api.com/v4/latest/USD',
            timeout=5
        )

    @patch.dict(os.environ, {
        'EXCHANGE_RATE_API_URL': 'https://custom-api.com/v4/latest',
        'EXTERNAL_API_TIMEOUT': '10',
        'STAGE': 'dev'
    })
    @patch('external_api.requests.get')
    def test_custom_api_url_and_timeout(self, mock_requests_get, sample_rates_response):
        importlib.reload(external_api)
        
        mock_response = Mock()
        mock_response.json.return_value = sample_rates_response
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        rates = external_api.get_latest_rates('USD')
        
        assert rates == sample_rates_response['rates']
        mock_requests_get.assert_called_once_with(
            'https://custom-api.com/v4/latest/USD',
            timeout=10
        )

    @patch.dict(os.environ, {'EXTERNAL_API_TIMEOUT': '5'})
    @patch('external_api.requests.get')
    def test_timeout_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.Timeout()
        
        with pytest.raises(ConnectionError) as exc_info:
            get_latest_rates('USD')
        
        assert 'Timeout while fetching rates' in str(exc_info.value)

    @patch.dict(os.environ, {'EXTERNAL_API_TIMEOUT': '5'})
    @patch('external_api.requests.get')
    def test_http_404_error(self, mock_requests_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            get_latest_rates('INVALID')
        
        assert 'Currency INVALID not supported' in str(exc_info.value)

    @patch.dict(os.environ, {'EXTERNAL_API_TIMEOUT': '5'})
    @patch('external_api.requests.get')
    def test_http_500_error(self, mock_requests_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(ConnectionError) as exc_info:
            get_latest_rates('USD')
        
        assert 'HTTP error 500' in str(exc_info.value)

    @patch.dict(os.environ, {'EXTERNAL_API_TIMEOUT': '5'})
    @patch('external_api.requests.get')
    def test_invalid_response_missing_rates(self, mock_requests_get):
        mock_response = Mock()
        mock_response.json.return_value = {'base': 'USD', 'date': '2024-01-01'}
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(ValueError) as exc_info:
            get_latest_rates('USD')
        
        assert 'Invalid response format' in str(exc_info.value)

    @patch.dict(os.environ, {'EXTERNAL_API_TIMEOUT': '5'})
    @patch('external_api.requests.get')
    def test_request_exception(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.RequestException('Connection failed')
        
        with pytest.raises(ConnectionError) as exc_info:
            get_latest_rates('USD')
        
        assert 'Failed to fetch rates' in str(exc_info.value)

    @patch.dict(os.environ, {'EXTERNAL_API_TIMEOUT': '5'})
    @patch('external_api.requests.get')
    def test_connection_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.ConnectionError('Network error')
        
        with pytest.raises(ConnectionError) as exc_info:
            get_latest_rates('USD')
        
        assert 'Failed to fetch rates' in str(exc_info.value)

    @patch.dict(os.environ, {
        'EXCHANGE_RATE_API_URL': 'https://api.exchangerate-api.com/v4/latest',
        'EXTERNAL_API_TIMEOUT': '5',
        'STAGE': 'dev'
    })
    @patch('external_api.requests.get')
    def test_different_base_currency(self, mock_requests_get, sample_rates_response):
        importlib.reload(external_api)
        
        eur_rates = {
            'rates': {
                'EUR': 1.0,
                'USD': 1.09,
                'BRL': 5.65
            },
            'base': 'EUR'
        }
        mock_response = Mock()
        mock_response.json.return_value = eur_rates
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        rates = external_api.get_latest_rates('EUR')
        
        assert rates == eur_rates['rates']
        mock_requests_get.assert_called_once_with(
            'https://api.exchangerate-api.com/v4/latest/EUR',
            timeout=5
        )

