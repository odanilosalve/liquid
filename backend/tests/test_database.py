import pytest
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal
from exceptions import DatabaseError
from database import get_conversion_rate, save_rate_to_cache, ExternalAPIUnavailableError


class TestSaveRateToCache:
    @patch('database.table')
    def test_save_successful(self, mock_table):
        save_rate_to_cache('USD', 'BRL', 5.2, 'test-request-id')
        
        mock_table.put_item.assert_called_once()
        call_args = mock_table.put_item.call_args[1]['Item']
        assert call_args['from_currency'] == 'USD'
        assert call_args['to_currency'] == 'BRL'
        assert call_args['rate'] == Decimal('5.2')

    @patch('database.table')
    def test_save_error(self, mock_table):
        mock_table.put_item.side_effect = Exception('Database error')
        
        with pytest.raises(DatabaseError):
            save_rate_to_cache('USD', 'BRL', 5.2, 'test-request-id')
        
        mock_table.put_item.assert_called_once()


class TestGetConversionRate:
    @patch('database.table')
    def test_cache_hit(self, mock_table, sample_dynamodb_item):
        mock_table.get_item.return_value = sample_dynamodb_item
        
        rate = get_conversion_rate('USD', 'BRL', 'test-request-id')
        
        assert rate == 5.2
        mock_table.get_item.assert_called_once_with(
            Key={
                'from_currency': 'USD',
                'to_currency': 'BRL'
            }
        )

    @patch('database.table')
    @patch('database.get_latest_rates')
    def test_cache_miss_fetch_from_api(self, mock_get_latest_rates, mock_table):
        mock_table.get_item.return_value = {}
        mock_table.put_item.return_value = None
        mock_get_latest_rates.return_value = {
            'USD': 1.0,
            'BRL': 5.2,
            'EUR': 0.92
        }
        
        rate = get_conversion_rate('USD', 'BRL', 'test-request-id')
        
        assert rate == 5.2
        mock_get_latest_rates.assert_called_once_with('USD', 'test-request-id')
        mock_table.put_item.assert_called_once()

    @patch('database.table')
    @patch('database.get_latest_rates')
    def test_currency_not_found_in_api_response(self, mock_get_latest_rates, mock_table):
        mock_table.get_item.return_value = {}
        mock_get_latest_rates.return_value = {
            'USD': 1.0,
            'EUR': 0.92
        }
        
        with pytest.raises(ValueError) as exc_info:
            get_conversion_rate('USD', 'BRL', 'test-request-id')
        
        assert 'Conversion rate not found for USD to BRL' in str(exc_info.value)

    @patch('database.table')
    @patch('database.get_latest_rates')
    def test_external_api_unavailable(self, mock_get_latest_rates, mock_table):
        mock_table.get_item.return_value = {}
        mock_get_latest_rates.side_effect = ConnectionError('API unavailable')
        
        with pytest.raises(ExternalAPIUnavailableError) as exc_info:
            get_conversion_rate('USD', 'BRL', 'test-request-id')
        
        assert 'External API unavailable' in str(exc_info.value)

    @patch('database.table')
    @patch('database.get_latest_rates')
    def test_different_currencies(self, mock_get_latest_rates, mock_table):
        mock_table.get_item.return_value = {}
        mock_table.put_item.return_value = None
        mock_get_latest_rates.return_value = {
            'EUR': 1.0,
            'USD': 1.09,
            'BRL': 5.65,
            'JPY': 163.04
        }
        
        rate = get_conversion_rate('EUR', 'JPY', 'test-request-id')
        
        assert rate == 163.04
        mock_get_latest_rates.assert_called_once_with('EUR', 'test-request-id')

    @patch('database.table')
    def test_dynamodb_error(self, mock_table):
        mock_table.get_item.side_effect = Exception('DynamoDB error')
        
        with pytest.raises(DatabaseError) as exc_info:
            get_conversion_rate('USD', 'BRL', 'test-request-id')
        
        assert 'while fetching rate' in str(exc_info.value)

    @patch('database.table')
    @patch('database.get_latest_rates')
    def test_cache_miss_saves_to_cache(self, mock_get_latest_rates, mock_table):
        mock_table.get_item.return_value = {}
        mock_table.put_item.return_value = None
        mock_get_latest_rates.return_value = {'BRL': 5.2}
        
        rate = get_conversion_rate('USD', 'BRL', 'test-request-id')
        
        assert rate == 5.2
        mock_table.put_item.assert_called_once()
        call_args = mock_table.put_item.call_args[1]['Item']
        assert call_args['from_currency'] == 'USD'
        assert call_args['to_currency'] == 'BRL'
        assert call_args['rate'] == Decimal('5.2')

