
class HTTPMethod:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
    HEAD = 'HEAD'
    PATCH = 'PATCH'


class BusinessName:
    VR = 'vr'


class RecordStatus:
    START = 'start'
    STOP = 'stop'
    PAUSE = 'pause'


class CollectionType:
    FLOW = 'flow'
    SET = 'set'


API_FILTER = {
    BusinessName.VR: '~u ^https://www.baidu.com/api.+'
}


