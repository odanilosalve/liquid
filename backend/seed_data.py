import boto3
import json
import logging
from decimal import Decimal
import os
from botocore.exceptions import BotoCoreError, ClientError
from exceptions import DatabaseError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = 'us-east-1'
STAGE = os.environ.get('STAGE', 'dev')
TABLE_NAME = f'currency-rates-{STAGE}'

CURRENCY_RATES = [
    ('USD', 'BRL', 5.20),
    ('USD', 'EUR', 0.92),
    ('USD', 'GBP', 0.79),
    ('USD', 'JPY', 150.00),
    ('BRL', 'USD', 0.19),
    ('BRL', 'EUR', 0.18),
    ('BRL', 'GBP', 0.15),
    ('BRL', 'JPY', 28.85),
    ('EUR', 'USD', 1.09),
    ('EUR', 'BRL', 5.65),
    ('EUR', 'GBP', 0.86),
    ('EUR', 'JPY', 163.04),
    ('GBP', 'USD', 1.27),
    ('GBP', 'BRL', 6.58),
    ('GBP', 'EUR', 1.16),
    ('GBP', 'JPY', 189.87),
    ('JPY', 'USD', 0.0067),
    ('JPY', 'BRL', 0.035),
    ('JPY', 'EUR', 0.0061),
    ('JPY', 'GBP', 0.0053),
]

def seed_table():
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(TABLE_NAME)
    
    logger.info(f'Populating table {TABLE_NAME}...')
    
    items_added = 0
    for from_currency, to_currency, rate in CURRENCY_RATES:
        try:
            table.put_item(
                Item={
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'rate': Decimal(str(rate))
                }
            )
            items_added += 1
            logger.info(f'Added: {from_currency} -> {to_currency} = {rate}')
        except (BotoCoreError, ClientError) as e:
            logger.error(f'Database error adding {from_currency} -> {to_currency}: {e}')
        except (ValueError, TypeError) as e:
            logger.error(f'Invalid data error adding {from_currency} -> {to_currency}: {e}')
        except Exception as e:
            logger.error(f'Unexpected error adding {from_currency} -> {to_currency}: {e}')
    
    logger.info(f'Total of {items_added} rates added to table {TABLE_NAME}')

if __name__ == '__main__':
    seed_table()

