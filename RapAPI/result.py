import uuid
import json

__all__ = ['Result']


class Result:
    def __init__(self, record_id):
        self._result_id = uuid.uuid1().hex
        self._record_id = record_id
        self.url = None
        self._status = None
        self._reason = None
        self._detail = []
        self._is_finished = False

    @property
    def result_id(self):
        return self._result_id

    @property
    def record_id(self):
        return self._record_id

    @property
    def status(self):
        return self._status

    @property
    def reason(self):
        return self._reason

    @property
    def detail(self):
        return self._detail

    @property
    def is_finished(self):
        return self._is_finished

    @status.setter
    def status(self, value):
        self._status = value

    @reason.setter
    def reason(self, value):
        self._reason = value

    @is_finished.setter
    def is_finished(self, value):
        self._is_finished = value

    @property
    def output(self):
        return {
            'result_id': self._result_id,
            'record_id': self._record_id,
            'status': self._status,
            'reason': self._reason,
            'detail': self._detail,
            'is_finished': self._is_finished,
            'url': self.url
        }

    def append(self, value):
        self._detail.append(value)

    def __str__(self):
        return json.dumps(self.output)

    def __repr__(self):
        if self.status:
            return 'OK'
        else:
            return f'Fail {self.url}'
