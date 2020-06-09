from enum import Enum


class ActionType(Enum):
    DOWNLOAD = 'download'
    UPLOAD = 'upload'
    BEGIN_UPLOAD = 'begin upload'
