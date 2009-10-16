import inspect

def available_exceptions():
    module= inspect.getmodule(BaseMeaningtoolError)
    return [obj for (name, obj) in inspect.getmembers(module) \
            if inspect.isclass(obj) and issubclass(obj, BaseMeaningtoolError)]

class BaseMeaningtoolError(Exception):
    """ Base exception from where all the others exceptions extends.
    """
    
    @classmethod
    def get_code(cls):
        """
        Returns a string codification of `cls`
        """
        return cls.__name__

    @staticmethod
    def from_code(code):
        """
        Returns an exception (subclass of ScoringError) matching the given `code`. 
        If no exception found, raises `UnknownExceptionCodeError`.

        :parameters:
          code : str
        """
        for exception in available_exceptions():
            if exception.get_code() == code:
                return exception()
        else:
            raise UnknownExceptionCodeError("No exception with code: %s" % code)

 


class InvalidParameter(BaseMeaningtoolError):
    """ Exception raised when a parameter of the client had an invalid value.
    """
    message = u"A parameter has an invalid value."

class InvalidUrl(InvalidParameter):
    """ Exception raises when a url is invalid. This can be happen
    on two situations:
        - the input is an url.
        - the `url_hint` parameter was used.
    """
    message = u"The url is invalid."


class UnknownExceptionCodeError(BaseMeaningtoolError): 
    """ Raises when the code from which get the real exception in invalid.
    """
    pass

class UndispatchableRequestScoringError(BaseMeaningtoolError):
    #TODO: remove. Shouldn't happen.
    message = u"Could not dispatch this request"

class MissingComponentsScoringError(BaseMeaningtoolError):
    #TODO: remove. Shouldn't happen.
    message = u"I don't know how to classify (some components are missing)"

class ScoringError(BaseMeaningtoolError):
    """ Generic error raised when the response has error status.
    """
    message = u"Generic scoring error"

       
 
class NoTextScoringError(ScoringError):
    message = u"The object appears to have no relevant text"

class NoClassifiersScoringError(ScoringError):
    message = u"No classifier matches this object"

class CannotDetectLanguageScoringError(ScoringError):
    message = u"Cannot detect the language of the text"


class InternalError(ScoringError):
    message = u"There was an error while categorizing."

class InvalidKey(ScoringError):
    """ Raised when there is an error with the user used in the client.
    """
    message = u"The user is invalid."

class LimitsExceeded(InvalidKey):
    message = u"API usage limits exceeded"

class ContractNotActive(InvalidKey):
    message = u"Your API key isn't enabled yet"

class CategoryTreeNotFound(InvalidKey):
    message = u"No category tree found with the specified ct-key."

class CategoryKeyInvalid(InvalidKey):
    message = u"The category doesn't belongs to the user and it isn't public."

class UserKeyInvalid(InvalidKey):
    message = u"Invalid API key"

class UrlClientError(BaseMeaningtoolError):
    """ Exception thrown when there was a 40X when getting the url data.
    This is thrown only when trying to extract the data from the input
    and the input is an url, and when fetched the url a 40X http error
    is returned.
    """
    message = u"Can't fetch the url."

class UrlDestinationServerError(BaseMeaningtoolError):
    """ Exception raised when there is a 50X when getting the url.
    This is similar to the UrlClientError, but in this case a 50X http error
    is returned.
    """
    message = u"Destination Server error while accessing the url."

class UrlTimeoutError(BaseMeaningtoolError):
    """ Exception raised when there was a timeout when getting the url.
    """
    message = u"Timeout while accessing the url."
