import os
import requests
import logging
from exceptions import ConfigurationError
from utils.logging_helpers import create_log_extra
from utils.config_validator import is_production

logger = logging.getLogger()

def get_api_base_url():
    url = os.environ.get('EXCHANGE_RATE_API_URL')
    if not url:
        if is_production():
            raise ConfigurationError('EXCHANGE_RATE_API_URL environment variable is required in production')
        return 'https://api.exchangerate-api.com/v4/latest'
    return url

def get_request_timeout():
    timeout_str = os.environ.get('EXTERNAL_API_TIMEOUT')
    if not timeout_str:
        if is_production():
            raise ConfigurationError('EXTERNAL_API_TIMEOUT environment variable is required in production')
        return 5
    return int(timeout_str)

API_BASE_URL = get_api_base_url()
REQUEST_TIMEOUT = get_request_timeout()


def get_latest_rates(base_currency, request_id=None):
    logger.info('Fetching rates from external API', extra=create_log_extra(
        request_id,
        base_currency=base_currency,
        api_url=f'{API_BASE_URL}/{base_currency}'
    ))
    
    try:
        response = requests.get(
            f'{API_BASE_URL}/{base_currency}',
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        
        if 'rates' not in data:
            logger.warning('Invalid response format from external API', extra=create_log_extra(
                request_id,
                base_currency=base_currency,
                response_keys=list(data.keys()) if isinstance(data, dict) else None
            ))
            raise ValueError(f'Invalid response format from external API for {base_currency}')
        
        rates = data['rates']
        
        logger.info('Successfully fetched rates from external API', extra=create_log_extra(
            request_id,
            base_currency=base_currency,
            rates_count=len(rates) if isinstance(rates, dict) else 0
        ))
        
        return rates
        
    except requests.exceptions.Timeout:
        logger.error('Timeout while fetching rates from external API', extra=create_log_extra(
            request_id,
            base_currency=base_currency,
            timeout_seconds=REQUEST_TIMEOUT
        ), exc_info=True)
        raise ConnectionError(f'Timeout while fetching rates for {base_currency}')
        
    except requests.exceptions.HTTPError as http_error:
        status_code = http_error.response.status_code if http_error.response else None
        logger.error('HTTP error while fetching rates from external API', extra=create_log_extra(
            request_id,
            base_currency=base_currency,
            status_code=status_code
        ), exc_info=True)
        
        if status_code == 404:
            raise ValueError(f'Currency {base_currency} not supported by external API')
        else:
            raise ConnectionError(f'HTTP error {status_code} while fetching rates for {base_currency}')
            
    except requests.exceptions.RequestException as req_error:
        logger.error('Request error while fetching rates from external API', extra=create_log_extra(
            request_id,
            base_currency=base_currency,
            error_type=type(req_error).__name__
        ), exc_info=True)
        raise ConnectionError(f'Failed to fetch rates for {base_currency}: {str(req_error)}')
        
    except ValueError:
        raise
    except Exception as e:
        logger.error('Unexpected error while fetching rates from external API', extra=create_log_extra(
            request_id,
            base_currency=base_currency,
            error_type=type(e).__name__
        ), exc_info=True)
        raise ConnectionError(f'Unexpected error while fetching rates for {base_currency}')

