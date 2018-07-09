import datetime
import unittest

import vcr
from freezegun import freeze_time

from eodclient.errors import InvalidExchangeCodeError
from eodclient.exchange import Exchange
from eodclient.symbol import Symbol


class ExchangeTests(unittest.TestCase):
    '''Tests for the exchange'''

    SYMBOL_KEYS = ['Code', 'Name', 'Country', 'Exchange', 'Currency']

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-symbols.yml',
        filter_query_parameters=['api_token']
    )
    def test_get_symbols(self):
        '''Ensure symbols are returned in correct format from the exchange'''
        exchange_instance = Exchange('JSE')
        response = exchange_instance.get_symbols()

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(
            list(response[0].keys()),
            self.SYMBOL_KEYS
        )

    def test_init_without_exchange_code(self):
        '''Ensure a no code exception is raised when initialising without
        a share code'''
        with self.assertRaises(TypeError):
            exchange_instance = Exchange()

    def test_init_bad_code(self):
        '''Ensure initialisng an exchange with a code that does not
        exist fails'''
        with self.assertRaises(InvalidExchangeCodeError):
            exchange_instance = Exchange('XXYP')


class SymbolTests(unittest.TestCase):
    '''Tests for the symbol'''

    @freeze_time('2018-07-03')
    def test_from_date(self):
        '''Test the from date of symbol'''
        symbol_instance = Symbol(code='AAPL', exchange_code='US')
        timediff = datetime.timedelta(days=378)
        from_date = symbol_instance.get_from_date(timediff)
        self.assertEqual(
            from_date,
            '2017-06-20'
        )
