import boto3
import json
from decimal import Decimal
import os

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
    
    print(f'Populando tabela {TABLE_NAME}...')
    
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
            print(f'✓ Adicionado: {from_currency} -> {to_currency} = {rate}')
        except Exception as e:
            print(f'✗ Erro ao adicionar {from_currency} -> {to_currency}: {e}')
    
    print(f'\n✅ Total de {items_added} taxas adicionadas à tabela {TABLE_NAME}')

if __name__ == '__main__':
    seed_table()

