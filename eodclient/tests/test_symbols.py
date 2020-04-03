import datetime
import unittest

import vcr

from eodclient.errors import (
    InvalidExchangeCodeError
)
from eodclient.exchange import Exchange
from eodclient.symbol import Symbol


class ExchangeTests(unittest.TestCase):
    '''Tests for the exchange'''

    SYMBOL_KEYS = ['Code', 'Name', 'Country', 'Exchange', 'Currency', 'Type']

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
        '''Ensure initialisng an exchange with a positional argument fails'''
        with self.assertRaises(InvalidExchangeCodeError):
            exchange_instance = Exchange('XXYP')

    def test_bad_code(self):
        with self.assertRaises(InvalidExchangeCodeError):
            Exchange_instance = Exchange(exchange_code='XXYP')


class SymbolTests(unittest.TestCase):
    '''Tests for the symbol'''

    def test_formatted_date(self):
        '''Ensure formatted date works'''
        str_date = '2018-08-20'
        date_object = Symbol.get_date(str_date)
        self.assertEqual(
            date_object,
            datetime.datetime(2018, 8, 20)
        )

    def test_unformatted_date(self):
        '''Ensure unformatted date fails'''
        str_date = '20-08-2018'
        with self.assertRaises(Exception):
            date_object = Symbol.get_date(str_date)

    def test_int_date(self):
        '''Ensure int date fails'''
        str_date = 2018
        with self.assertRaises(Exception):
            date_object = Symbol.get_date(str_date)

    @vcr.use_cassette(
        'eodclient/tests/vcr_cassettes/ticker-not-found.yml',
        filter_query_parameters=['api_token']
    )
    def test_ticker_not_found(self):
        '''Ensure ticker not found is handled'''
        exchange_instance = Exchange('NZ')
        response = exchange_instance.get_symbols()

        self.assertIsInstance(response, dict)
        self.assertEqual(
            response,
            {'message': 'Ticker Not Found'}
        )