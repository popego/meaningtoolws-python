import inspect

def available_exceptions():
    module= inspect.getmodule(ScoringError)
    return [obj for (name, obj) in inspect.getmembers(module) \
                        if inspect.isclass(obj) and issubclass(obj, ScoringError)]

class ScoringError(Exception):
    message = u"Generic scoring error"

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
        If no exception found, raises UnknownExceptionCodeError

        :parameters:
          code : str
        """
        for exception in available_exceptions():
            if exception.get_code() == code:
                return exception()
        else:
            raise UnknownExceptionCodeError()

        
class UnknownExceptionCodeError(Exception): pass

class NoTextScoringError(ScoringError):
    message = u"The object appears to have no relevant text"

class NoClassifiersScoringError(ScoringError):
    message = u"No classifier matches this object"

class MissingComponentsScoringError(ScoringError):
    message = u"I don't know how to classify (some components are missing)"

class CannotDetectLanguageScoringError(ScoringError):
    message = u"Cannot detect the language of the text"

class UndispatchableRequestScoringError(ScoringError):
    message = u"Could not dispatch this request"

class LimitsExceeded(ScoringError):
    message = u"API usage limits exceeded"

class ContractNotActive(ScoringError):
    message = u"Your API key isn't enabled yet"

class UserKeyInvalid(ScoringError):
    message = u"Invalid API key"

class InvalidArgumentsError(ScoringError):
    message = u"Some provided arguments are invalid"
