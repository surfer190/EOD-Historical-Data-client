from . import session


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


class SymbolSet(object):
    '''Class representing many stock symbols'''
    def __init__(self, symbol_list):
        '''Ensure the symbol list isa list of dicts'''
        if not isinstance(symbol_list, list):
            raise ValueError("must be initialised with a list of dicts")
        index = 0
        self.symbols = []
        for symbol in symbol_list:
            if not isinstance(symbol, dict):
                raise ValueError(
                    "all items in the list must be dicts "
                    f"(found at index { index }"
                    )
            else:
                self.symbols.append(Symbol(**symbol))
            index += 1

    def get_real_time(self):
        '''Split the data into chunks of 15 shares and make requests
        combine at the end'''
        results = []
        for chunk in chunks(self.symbols, 15):
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
            results = results + result
        return results


def chunks(list_, n):
    '''Split the list into chunks of n'''
    for i in range(0, len(list_), n):
        yield list_[i:i+n]
