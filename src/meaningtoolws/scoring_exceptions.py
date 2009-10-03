import inspect

def available_exceptions():
    module= inspect.getmodule(BaseMeaningtoolError)
    return [obj for (name, obj) in inspect.getmembers(module) \
                        if inspect.isclass(obj) and issubclass(obj, BaseMeaningtoolError)]

class BaseMeaningtoolError(Exception):
    message = u"Generic error"

    @classmethod
    def get_code(cls):
        """
        Returns a string codification of `cls`
        """
        return cls.__name__

    @staticmethod
    def from_code(code):
        """
        Returns an exception (subclass of BaseMeaningtoolError) matching the given `code`. 
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

class ScoringError(BaseMeaningtoolError): pass

class NoTextScoringError(ScoringError):
    message = u"The object appears to have no relevant text"

class NoClassifiersScoringError(ScoringError):
    message = u"No classifier matches this object"

class MissingComponentsScoringError(BaseMeaningtoolError):
    # TODO Remove. Shouldn't happen
    message = u"I don't know how to classify (some components are missing)"

class CannotDetectLanguageScoringError(ScoringError):
    message = u"Cannot detect the language of the text"

class UndispatchableRequestScoringError(BaseMeaningtoolError):
    # TODO Remove. Shouldn't happen
    message = u"Could not dispatch this request"
