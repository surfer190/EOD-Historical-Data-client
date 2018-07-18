import datetime

from . import session
from .errors import (
    IncorrectDateFormatError,
    SymbolDictRequiredError,
    SymbolListRequiredError,
    SymbolNotFoundError
)

__all__ = ['Symbol', 'SymbolSet']


class Symbol(object):
    '''Class representing a single stock symbol'''
    def __init__(self, code, exchange_code):
        '''Set the code and exchange code'''
        self.code = code
        self.exchange_code = exchange_code

    def get_real_time(self):
        '''Get the real time data for a symbol'''
        path = 'https://eodhistoricaldata.com/api/real-time/' \
               f'{ self.code }.{ self.exchange_code }'
        response = session.get(
            path,
            params={'fmt': 'json'}
        )
        return response.json()

    @staticmethod
    def get_date(date):
        '''Convert a string date to a datetime'''
        try:
            date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise IncorrectDateFormatError('Date must be in format %Y-%m-%d')
        else:
            return date_object

    def get_end_of_day(self, *, from_date=None, **kwargs):
        '''Get end of day data for a symbol'''
        params = {'fmt': 'json'}

        if from_date:
            date_object = self.get_date(from_date)
            params['from'] = date_object.strftime('%Y-%m-%d')

        path = 'https://eodhistoricaldata.com/api/eod/' \
               f'{ self.code }.{ self.exchange_code }'
        response = session.get(
            path,
            params=params
        )
        if response.status_code == 404:
            raise SymbolNotFoundError()
        return response.json()


class SymbolSet(object):
    '''Class representing many stock symbols'''
    def __init__(self, symbol_list):
        '''Ensure the symbol list isa list of dicts'''
        if not isinstance(symbol_list, list):
            raise SymbolListRequiredError("must be initialised with a list of dicts")
        self.symbols = []
        for index, symbol in enumerate(symbol_list):
            if not isinstance(symbol, dict):
                raise SymbolDictRequiredError(
                    "all items in the list must be dicts "
                    f"(found at index { index })"
                    )
            else:
                self.symbols.append(Symbol(**symbol))

    def get_real_time(self):
        '''Split the data into chunks of 20 shares and make requests
        combine at the end'''
        results = []
        for chunk in chunks(self.symbols, 20):
            first = chunk[0]
            path = 'https://eodhistoricaldata.com/api/real-time/' \
                f'{ first.code }.{ first.exchange_code }'
            the_rest_string = ','.join(
                [f'{s.code}.{s.exchange_code}' for s in chunk[1:]]
            )
            response = session.get(
                path,
                params={
                    'fmt': 'json',
                    's': the_rest_string
                }
            )
            result = response.json()
            if isinstance(result, dict):
                result = [result]
            results = results + result
        return results


def chunks(list_, number):
    '''Split the list into chunks of n'''
    for i in range(0, len(list_), number):
        yield list_[i:i + number]
