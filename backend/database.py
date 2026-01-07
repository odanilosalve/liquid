import os
import time
import boto3
import logging
from decimal import Decimal
from botocore.exceptions import BotoCoreError, ClientError
from external_api import get_latest_rates
from exceptions import DatabaseError, ExternalAPIError, ConfigurationError
from utils.logging_helpers import create_log_extra
from utils.error_handlers import handle_database_error
from utils.config_validator import is_production

logger = logging.getLogger()


class ExternalAPIUnavailableError(ExternalAPIError):
    pass

def get_dynamodb_resource():
    region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    return boto3.resource('dynamodb', region_name=region)

dynamodb = get_dynamodb_resource()

def get_currency_table_name():
    table_name = os.environ.get('CURRENCY_TABLE')
    if not table_name:
        if is_production():
            raise ConfigurationError('CURRENCY_TABLE environment variable is required in production')
        return 'currency-rates-dev'
    return table_name

table_name = get_currency_table_name()
table = dynamodb.Table(table_name)


def get_cache_ttl_hours():
    """Get cache TTL in hours from environment variable, defaulting to 1 hour."""
    ttl_str = os.environ.get('CACHE_TTL_HOURS', '1')
    try:
        return int(ttl_str)
    except (ValueError, TypeError):
        logger.warning(f'Invalid CACHE_TTL_HOURS value: {ttl_str}, using default 1 hour')
        return 1


def save_rate_to_cache(from_currency, to_currency, rate, request_id=None):
    """Save conversion rate to cache with TTL."""
    cache_ttl_hours = get_cache_ttl_hours()
    ttl_timestamp = int(time.time()) + (cache_ttl_hours * 3600)
    
    try:
        table.put_item(
            Item={
                'from_currency': from_currency,
                'to_currency': to_currency,
                'rate': Decimal(str(rate)),
                'ttl': ttl_timestamp
            }
        )
        logger.info('Rate saved to cache', extra=create_log_extra(
            request_id,
            from_currency=from_currency,
            to_currency=to_currency,
            rate=rate,
            ttl_hours=cache_ttl_hours,
            expires_at=ttl_timestamp
        ))
    except (BotoCoreError, ClientError) as e:
        logger.warning('Failed to save rate to cache', extra=create_log_extra(
            request_id,
            from_currency=from_currency,
            to_currency=to_currency,
            error_type=type(e).__name__
        ))
        raise DatabaseError(f'Failed to save rate to cache: {str(e)}')
    except Exception as e:
        logger.warning('Failed to save rate to cache', extra=create_log_extra(
            request_id,
            from_currency=from_currency,
            to_currency=to_currency,
            error_type=type(e).__name__
        ))
        raise DatabaseError(f'Failed to save rate to cache: {str(e)}')


def get_conversion_rate(from_currency, to_currency, request_id=None):
    logger.debug('Querying DynamoDB for conversion rate', extra=create_log_extra(
        request_id,
        from_currency=from_currency,
        to_currency=to_currency,
        table_name=table_name
    ))
    
    try:
        response = table.get_item(
            Key={
                'from_currency': from_currency,
                'to_currency': to_currency
            }
        )
    except (BotoCoreError, ClientError) as e:
        handle_database_error(e, request_id, f'while fetching rate for {from_currency} to {to_currency}')
    except Exception as e:
        handle_database_error(e, request_id, f'while fetching rate for {from_currency} to {to_currency}')
    
    if 'Item' in response:
        rate = float(response['Item']['rate'])
        logger.info('Rate found in cache', extra=create_log_extra(
            request_id,
            from_currency=from_currency,
            to_currency=to_currency,
            rate=rate,
            source='cache'
        ))
        return rate
    
    logger.info('Rate not found in cache, fetching from external API', extra=create_log_extra(
        request_id,
        from_currency=from_currency,
        to_currency=to_currency
    ))
    
    try:
        rates = get_latest_rates(from_currency, request_id)
        
        if to_currency not in rates:
            logger.warning('Target currency not found in API response', extra=create_log_extra(
                request_id,
                from_currency=from_currency,
                to_currency=to_currency,
                available_currencies=list(rates.keys())[:10] if isinstance(rates, dict) else None
            ))
            raise ValueError(f'Conversion rate not found for {from_currency} to {to_currency}')
        
        rate = float(rates[to_currency])
        
        save_rate_to_cache(from_currency, to_currency, rate, request_id)
        
        logger.info('Rate fetched from external API and cached', extra=create_log_extra(
            request_id,
            from_currency=from_currency,
            to_currency=to_currency,
            rate=rate,
            source='external_api'
        ))
        
        return rate
        
    except ValueError:
        raise
    except ConnectionError as conn_error:
        logger.error('Failed to fetch rate from external API', extra=create_log_extra(
            request_id,
            from_currency=from_currency,
            to_currency=to_currency,
            error=str(conn_error)
        ), exc_info=True)
        raise ExternalAPIUnavailableError(f'External API unavailable: {str(conn_error)}')
    except (BotoCoreError, ClientError) as e:
        handle_database_error(e, request_id, f'while fetching rate for {from_currency} to {to_currency}')
    except Exception as e:
        handle_database_error(e, request_id, f'while fetching rate for {from_currency} to {to_currency}')


