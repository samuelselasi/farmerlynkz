class BaseException(Exception):
    def __init__(self, message:str=None):
        self.message = message
    
    def _message(self):
        return self.message

class NotFoundError(BaseException):
    pass

class UnAcceptableError(BaseException):
    pass

class UnAuthorised(BaseException):
    pass

class ExpectationFailure(BaseException):
    pass

class FileReadFailed(BaseException):
    pass

class FileNameError(BaseException):
    pass

class MaxOccurrenceError(BaseException):
    pass

class CreateFolderError(BaseException):
    pass
