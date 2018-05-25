# EOD-Historical-Data-client

A client for interacting with [https://eodhistoricaldata.com/](https://eodhistoricaldata.com/)

## Run the tests

    EOD_API_KEY='your-key-here' nosetests -s

Use `-s` for stdout of `pdb` to be output immediately

Sometimes it is easier to add your key to the environment

## Structure

* Exchange - name, code
* Symbol - Code, Country, Currency, Exchange, Name

## Getting Started

    pip install eodclient

## Usage

### Get Symbols

    from eodclient import exchange

    us_exchange = exchange.Exchange('US')
    us_exchange.get_symbols()

## Get Real time data for a single symbol

    from eodclient.symbol import Symbol

    apple_symbol = Symbol(code='AAPL', exchange_code='US')
    apple_data = apple_symbol.get_real_time()

## Get Real time data for multiple stocks

    from eodclient.symbol import SymbolSet

    symbols = SymbolSet(
        [
            {'code': 'AAPL', 'exchange_code': 'US'},
            {'code': 'PLKT', 'exchange_code': 'US'},
            {'code': 'WHL', 'exchange_code': 'JSE'},
        ]
    )
    data = symbols.get_real_time()

## Uploading to pYpi

1. Update the readme and version in `setup.py`

2. Create the git tag locally

    git tag -a 1.0.5.dev1 -m "Real time data"
    git push origin 1.0.5.dev1

3. Distribute and update pypi

    python setup.py sdist upload