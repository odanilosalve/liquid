import json
import logging

logger = logging.getLogger()


def parse_request_body(event):
    if isinstance(event.get('body'), str):
        return json.loads(event['body'])
    else:
        return event.get('body', {})


def extract_request_data(body):
    amount = body.get('amount')
    from_currency = body.get('from', '').upper()
    to_currency = body.get('to', '').upper()
    return amount, from_currency, to_currency

