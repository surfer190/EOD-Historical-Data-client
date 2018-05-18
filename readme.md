# EOD-Historical-Data-client

A client for interacting with [https://eodhistoricaldata.com/](https://eodhistoricaldata.com/)

## Run the tests

    EOD_API_KEY='your-key-here' nosetests

Sometimes it is easier to add your key to the environment

## Structure

* Exchange - name, code
* Symbol - Code, Country, Currency, Exchange, Name

## Getting Started

    pip install eodclient

## Usage

    from eodclient import exchange

    us_exchange = exchange.Exchange('US')
    us_exchange.get_symbols()
