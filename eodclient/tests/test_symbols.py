import unittest
import vcr

from eodclient.errors import InvalidExchangeCodeError
from eodclient.exchange import Exchange


class ExchangeTests(unittest.TestCase):
    '''Tests for the exchange'''

    SYMBOL_KEYS = ['Code', 'Name', 'Country', 'Exchange', 'Currency']

    @vcr.use_cassette('tests/vcr_cassettes/get-symbols.yml', filter_query_parameters=['api_token'])
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
