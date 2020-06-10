from enum import Enum


class ActionType(Enum):
    DOWNLOAD = 'download'
    UPLOAD = 'upload'
    BEGIN_UPLOAD = 'begin upload'
    BEGIN_DOWNLOAD = 'begin download'
    FILE_NOT_FOUND = 'file not found'