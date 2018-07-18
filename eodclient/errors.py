
class Error(Exception):
    '''Base class for all exceptions raised by this module'''


class APIKeyMissingError(Error):
    '''The API key was Missing'''


class IncorrectDateFormatError(Error):
    '''The Date entered is formatted incorrectly'''


class SymbolListRequiredError(Error):
    '''A symbol list is required'''


class SymbolNotFoundError(Error):
    '''No Symbol Data'''


class SymbolDictRequiredError(Error):
    '''A symbol dict is required'''


class ExchangeCodeRequiredError(Error):
    '''An exchange code is required'''


class InvalidExchangeCodeError(Error):
    '''Exception raised for invalid exchange code supplied

        Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    '''

    def __init__(self, expression, message):
        super().__init__()
        self.expression = expression
        self.message = message
