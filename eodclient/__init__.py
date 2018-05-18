'''Initialise the eod client with api tokem in session'''

import os
import requests

EOD_API_KEY = os.environ.get('EOD_API_KEY', None)


class APIKeyMissingError(Exception):
    '''Generic API Missing exception class'''
    pass

if EOD_API_KEY is None:
    raise APIKeyMissingError(
        "All methods require an EOD_API_KEY env variable from "
        "https://eodhistoricaldata.com/"
    )
session = requests.Session()
session.params = {}
session.params['api_token'] = EOD_API_KEY
