from pydantic import BaseModel


class ClassificationTypes(BaseModel):
    classification_type: str


class create_classification_types(ClassificationTypes):
    pass


class CropTypes(BaseModel):
    classif_id: int
    crop_type: str


class create_crop_types(CropTypes):
    pass


class Crop(BaseModel):
    classif_id: int
    croptype_id: int
    cropname: str


class create_crop(Crop):
    pass


class BaseException(Exception):
    def __init__(self, message: str = None):
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
