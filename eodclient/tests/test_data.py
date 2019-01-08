import unittest

import vcr

from eodclient import *
from eodclient.errors import (
    IncorrectDateFormatError,
    SymbolNotFoundError
)


class DataTests(unittest.TestCase):
    '''Tests for getting the live data'''

    REALTIME_KEYS = [
        'code', 'timestamp', 'gmtoffset', 'open', 'high', 'low',
        'close', 'volume', 'previousClose', 'change', 'change_p']
    EOD_KEYS = [
        'date', 'open', 'high', 'low', 'close',
        'adjusted_close', 'volume', ]

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-single-realtime.yml',
        filter_query_parameters=['api_token']
    )
    def test_get_single_symbol(self):
        '''Test get a single symbol live data'''
        symbol_instance = Symbol(code='AAPL', exchange_code='US')
        response = symbol_instance.get_real_time()

        self.assertIsInstance(response, dict)
        self.assertEqual(
            list(response.keys()),
            self.REALTIME_KEYS
        )

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-single-eod.yml',
        filter_query_parameters=['api_token']
    )
    def test_get_eod_symbol(self):
        '''Test get a single symbol end of day data'''
        symbol_instance = Symbol(code='AAPL', exchange_code='US')
        response = symbol_instance.get_end_of_day()

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(
            list(response[0].keys()),
            self.EOD_KEYS
        )

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-single-eod-from.yml',
        filter_query_parameters=['api_token']
    )
    def test_get_eod_symbol_year(self):
        '''Test get a single symbol end of day data
        Since 2016-01-01
        '''
        symbol_instance = Symbol(code='AAPL', exchange_code='US')
        response = symbol_instance.get_end_of_day(from_date='2016-01-01')

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(
            list(response[0].keys()),
            self.EOD_KEYS
        )
        self.assertEqual(
            response[0]['date'],
            '2016-01-04'
        )

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-single-eod-from-tfg.yml',
        filter_query_parameters=['api_token']
    )
    def test_get_eod_symbol_tfg(self):
        '''Test get a single symbol end of day data
        Since 2018-02-04
        '''
        symbol_instance = Symbol(code='TFG', exchange_code='JSE')
        response = symbol_instance.get_end_of_day(from_date='2018-02-04')

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(
            list(response[0].keys()),
            self.EOD_KEYS
        )
        self.assertEqual(
            response[0]['date'],
            '2018-02-05'
        )

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-single-eod-404.yml',
        filter_query_parameters=['api_token']
    )
    def test_symbol_not_found_eod(self):
        '''Test get a single symbol end of day data
        with no json (decodeError)
        '''
        symbol_instance = Symbol(code='J055', exchange_code='JSE')
        with self.assertRaises(SymbolNotFoundError):
            response = symbol_instance.get_end_of_day(from_date='2018-02-04')

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-single-eod-bad-from.yml',
        filter_query_parameters=['api_token']
    )
    def test_get_eod_bad_from(self):
        '''Test get a single symbol with a bad from
        '''
        symbol_instance = Symbol(code='AAPL', exchange_code='US')
        with self.assertRaises(IncorrectDateFormatError):
            response = symbol_instance.get_end_of_day(from_date='01-01-2016')

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

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-realtime-small.yml',
        filter_query_parameters=['api_token']
    )
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

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-realtime-large.yml',
        filter_query_parameters=['api_token']
    )
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

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-realtime-15.yml',
        filter_query_parameters=['api_token']
    )
    def test_16_codes(self):
        '''Ensure a symbol list splits queries for 16'''
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
            ]
        )
        response = symbol_set_instance.get_real_time()

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(
            len(response),
            16
        )

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-multiple.yml',
        filter_query_parameters=['api_token']
    )
    def test_correct_code_queried(self):
        '''Ensure the correct code is queried'''
        symbolset = SymbolSet([
            {'code': 'SGL', 'exchange_code': 'JSE'},
            {'code': 'CML', 'exchange_code': 'JSE'},
            {'code': 'AAPL', 'exchange_code': 'US'}
        ])
        response = symbolset.get_real_time()
        self.assertEqual(
            response[0]['code'],
            'SGL.JSE'
        )
        self.assertEqual(
            response[1]['code'],
            'CML.JSE'
        )
        self.assertEqual(
            response[2]['code'],
            'AAPL.US'
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

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-realtime-unknown.yml',
        filter_query_parameters=['api_token']
    )
    def test_unknown_codes(self):
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

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/get-realtime-single.yml',
        filter_query_parameters=['api_token']
    )
    def test_single_symbolset(self):
        '''Test getting a single symbol with a set'''
        symbol_set_instance = SymbolSet(
            [
                {'code': 'AAPL', 'exchange_code': 'US'},
            ]
        )
        response = symbol_set_instance.get_real_time()
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(
            list(response[0].keys()),
            self.REALTIME_KEYS
        )
