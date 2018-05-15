from . import session


class Exchange(object):
    '''Exchange object for interacting with the EOD exchange'''
    def __init__(self, exchange):
        '''The exchange code from
        https://eodhistoricaldata.com/knowledgebase/list-supported-exchanges/
        is required'''
        self.exchange = exchange

    def get_symbols(self):
        '''Get all the symbols in the exchange'''
        path = f'https://eodhistoricaldata.com/api/exchanges/{self.exchange}'
        response = session.get(
            path,
            params={'fmt': 'json'}
        )
        return response.json()
