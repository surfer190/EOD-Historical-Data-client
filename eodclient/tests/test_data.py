import unittest
import vcr

from eodclient.symbol import Symbol, SymbolSet


class DataTests(unittest.TestCase):
    '''Tests for getting the live data'''

    REALTIME_KEYS = [
        'code', 'timestamp', 'gmtoffset', 'open', 'high', 'low',
        'close', 'volume', 'previousClose', 'change']

    @vcr.use_cassette('eodclient/tests/vcr_cassettes/get-single-realtime.yml', filter_query_parameters=['api_token'])
    def test_get_single_symbol(self):
        '''Test get a single symbol live data'''
        symbol_instance = Symbol(code='AAPL', exchange_code='US')
        response = symbol_instance.get_real_time()

        self.assertIsInstance(response, dict)
        self.assertEqual(
            list(response.keys()),
            self.REALTIME_KEYS
        )

    def test_init_without_params(self):
        '''Ensure a no code exception is raised when initialising without
        a share code'''
        with self.assertRaises(TypeError):
            symbol_instance = Symbol(code='whl')

    def test_init_without_exchange_code(self):
        '''Ensure a no code exception is raised when initialising without
        an exchange code'''
        with self.assertRaises(TypeError):
            symbol_instance = Symbol()

    @vcr.use_cassette('eodclient/tests/vcr_cassettes/get-realtime-small.yml', filter_query_parameters=['api_token'])
    def test_get_many_symbols(self):
        '''Test getting multiple symbol data'''
        symbol_set_instance = SymbolSet(
            [
                {'code': 'AAPL', 'exchange_code': 'US'},
                {'code': 'PLKT', 'exchange_code': 'US'},
                {'code': 'WHL', 'exchange_code': 'JSE'},
            ]
        )
        response = symbol_set_instance.get_real_time()

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(
            list(response[0].keys()),
            self.REALTIME_KEYS
        )

    @vcr.use_cassette('eodclient/tests/vcr_cassettes/get-realtime-large.yml', filter_query_parameters=['api_token'])
    def test_more_than_15_split(self):
        '''Ensure a symbol list splits queries if more than 15'''
        symbol_set_instance = SymbolSet(
            [
                {'code': 'AAPL', 'exchange_code': 'US'},
                {'code': 'ABT', 'exchange_code': 'US'},
                {'code': 'ACCO', 'exchange_code': 'US'},
                {'code': 'AEF', 'exchange_code': 'US'},
                {'code': 'PLKT', 'exchange_code': 'US'},
                {'code': 'BBY', 'exchange_code': 'LSE'},
                {'code': 'BGS', 'exchange_code': 'LSE'},
                {'code': 'BLV', 'exchange_code': 'LSE'},
                {'code': 'CASH', 'exchange_code': 'LSE'},
                {'code': 'CLP', 'exchange_code': 'LSE'},
                {'code': 'BB', 'exchange_code': 'TO'},
                {'code': 'ATI', 'exchange_code': 'V'},
                {'code': 'AMT', 'exchange_code': 'BE'},
                {'code': 'COK', 'exchange_code': 'HM'},
                {'code': 'BAS', 'exchange_code': 'XETRA'},
                {'code': 'ALE', 'exchange_code': 'DU'},
                {'code': 'CCL', 'exchange_code': 'MU'},
                {'code': 'CVA', 'exchange_code': 'STU'},
                {'code': '8BI', 'exchange_code': 'F'},
                {'code': 'PAL', 'exchange_code': 'VI'},
                {'code': 'BO', 'exchange_code': 'MI'},
                {'code': 'ATO', 'exchange_code': 'PA'},
                {'code': 'FP', 'exchange_code': 'BR'},
                {'code': 'LLN', 'exchange_code': 'MC'},
                {'code': 'KA', 'exchange_code': 'AS'},
                {'code': 'ROG', 'exchange_code': 'VX'},
                {'code': 'GPA', 'exchange_code': 'LS'},
                {'code': 'GE', 'exchange_code': 'SW'},
                {'code': 'CE', 'exchange_code': 'ST'},
                {'code': 'SPU', 'exchange_code': 'OL'},
                {'code': 'DANT', 'exchange_code': 'CO'},
                {'code': 'AM1', 'exchange_code': 'HE'},
                {'code': 'WHL', 'exchange_code': 'JSE'},
            ]
        )
        response = symbol_set_instance.get_real_time()

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(
            len(response),
            33
        )

    def test_init_without_list(self):
        '''Ensure a list of dicts is required'''
        with self.assertRaises(TypeError):
            symbol_set_instance = SymbolSet()

    def test_init_no_exchange(self):
        '''Error when no exchange given'''
        with self.assertRaises(TypeError):
            symbol_set_instance = SymbolSet(
                [
                    {'code': 'AAPL'},
                    {'code': 'PLKT'},
                    {'code': 'WHL'},
                ]
            )

    @vcr.use_cassette('eodclient/tests/vcr_cassettes/get-realtime-unknown.yml', filter_query_parameters=['api_token'])
    def test_unknown_codes(self):
        '''Ensure a symbol list splits queries if more than 15'''
        symbol_set_instance = SymbolSet(
            [
                {'code': 'AAPL', 'exchange_code': 'BBL'},
                {'code': 'E4RNH', 'exchange_code': 'US'},
                {'code': 'ZBLN1', 'exchange_code': 'US'},
            ]
        )
        response = symbol_set_instance.get_real_time()

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(
            len(response),
            3
        )