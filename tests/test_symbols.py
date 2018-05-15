import unittest
import vcr

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
