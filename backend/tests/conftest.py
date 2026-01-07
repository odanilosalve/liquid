import pytest
from unittest.mock import Mock, MagicMock
import os


@pytest.fixture
def mock_dynamodb_table():
    mock_table = MagicMock()
    return mock_table


@pytest.fixture
def mock_dynamodb_resource(mocker, mock_dynamodb_table):
    mock_resource = MagicMock()
    mock_resource.Table.return_value = mock_dynamodb_table
    return mock_resource


@pytest.fixture
def sample_rates_response():
    return {
        'rates': {
            'USD': 1.0,
            'BRL': 5.2,
            'EUR': 0.92,
            'GBP': 0.79,
            'JPY': 150.0
        },
        'base': 'USD',
        'date': '2024-01-01'
    }


@pytest.fixture
def sample_dynamodb_item():
    return {
        'Item': {
            'from_currency': 'USD',
            'to_currency': 'BRL',
            'rate': 5.2
        }
    }

