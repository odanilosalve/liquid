import os
import boto3
import logging

logger = logging.getLogger()

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CURRENCY_TABLE', 'currency-rates-dev')
table = dynamodb.Table(table_name)


def get_conversion_rate(from_currency, to_currency, request_id=None):
    logger.debug('Querying DynamoDB for conversion rate', extra={
        'request_id': request_id,
        'from_currency': from_currency,
        'to_currency': to_currency,
        'table_name': table_name
    })
    
    response = table.get_item(
        Key={
            'from_currency': from_currency,
            'to_currency': to_currency
        }
    )
    
    if 'Item' not in response:
        logger.warning('Conversion rate not found in database', extra={
            'request_id': request_id,
            'from_currency': from_currency,
            'to_currency': to_currency
        })
        raise ValueError(f'Conversion rate not found for {from_currency} to {to_currency}')
    
    rate = float(response['Item']['rate'])
    return rate

