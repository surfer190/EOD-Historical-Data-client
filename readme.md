# EOD-Historical-Data-client

### Get exchange Symbols

`https://eodhistoricaldata.com/api/exchanges/{EXCHANGE_CODE}?api_token={YOUR_API_KEY}`

## Run the tests

    EOD_API_KEY='your-key-here' python -m unittest tests/test_symbols.py

Sometimes it is easier to add your key to the environment

## Structure

Exchange - name, code
Symbol - Code, Country, Currency, Exchange, Name