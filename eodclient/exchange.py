from .errors import InvalidExchangeCodeError

from . import session

EXCHANGE_CODES = [
    'US', 'LSE', 'TO', 'V', 'BE', 'HM', 'XETRA', 'DU', 'MU', 'HA',
    'STU', 'F', 'VI', 'MI', 'PA', 'BR', 'MC', 'AS', 'VX', 'LS', 
    'SW', 'ST', 'OL', 'CO', 'NB', 'NFN', 'IS', 'HE', 'IR', 'TA',
    'HK', 'MCX', 'AU', 'KO', 'NZ', 'NX', 'SG', 'BSE', 'NSE', 'SR',
    'BK', 'TSE', 'JSE', 'KAR', 'JK', 'SHG', 'SHE', 'KLSE', 'SA',
    'MX', 'IL', 'FOREX', 'COMM', 'INDX', 'CC', 'TW'
]


class Exchange(object):
    '''Exchange object for interacting with the EOD exchange'''
    def __init__(self, exchange_code):
        '''The exchange code from
        https://eodhistoricaldata.com/knowledgebase/list-supported-exchanges/
        is required'''
        if exchange_code not in EXCHANGE_CODES:
            codes = ','.join(EXCHANGE_CODES)
            raise InvalidExchangeCodeError(
                expression=exchange_code,
                message=f'Ensure exchange code is in: { codes }'
            )
        self.exchange_code = exchange_code

    def get_symbols(self):
        '''Get all the symbols in the exchange'''
        path = f'https://eodhistoricaldata.com/api/exchanges/{self.exchange_code}'
        response = session.get(
            path,
            params={'fmt': 'json'}
        )
        return response.json()
