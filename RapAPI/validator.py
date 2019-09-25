import json

from .utils import JsonEncoder, reset_jsonpath_value, is_node_empty

__all__ = ['Validator']


class Validator:
    def __init__(self, verify_type, result):
        self.verify_type = verify_type or ''
        self.result = result

    def verify(self, actual, expect, **kwargs):
        validator = getattr(self, self.verify_type, None)
        if not validator:
            self.result.append(f'Get validator by [{self.verify_type}] Fail, Use the default validator.')
            validator = self.equal
        else:
            self.result.append(f'Set validator with [{self.verify_type}]')

        validator(actual, expect, **kwargs)

    def json(self, actual, expect, **kwargs):
        try:
            actual['content'] = json.loads(actual['content'])
            expect['content'] = json.loads(expect['content'])
        except Exception as e:
            print(f'Exception In [Validator.json] {e}')

        if kwargs.get('exclude'):
            excludes = kwargs['exclude']
            for jsonp in excludes:
                reset_jsonpath_value(actual, jsonp, '')
                reset_jsonpath_value(expect, jsonp, '')
        if kwargs.get('not_empty'):
            not_empty_list = kwargs['not_empty']
            for jsonp in not_empty_list:
                actual_empty = is_node_empty(actual, jsonp)
                if actual_empty:
                    self.result.append(f'ERROR: Node Should Not Empty [{jsonp}]')
                    self.result.append(json.dumps(actual))
                    self.result.status = False
                    return
                else:
                    self.result.append(f'INFO: Replace unEmpty Node [{jsonp}]')
                    reset_jsonpath_value(actual, jsonp, '')
                    reset_jsonpath_value(expect, jsonp, '')

        self.equal(actual, expect, **kwargs)

    def equal(self, actual, expect, **kwargs):
        if type(actual) != type(expect):
            actual_str = str(actual)
            expect_str = str(expect)
        elif isinstance(actual, (str, bytes)) and isinstance(expect, (str, bytes)):
            actual_str = str(actual)
            expect_str= str(expect)
        elif isinstance(actual, dict) and isinstance(expect, dict):
            actual_str = json.dumps(actual, cls=JsonEncoder, ensure_ascii=False)
            expect_str = json.dumps(expect, cls=JsonEncoder, ensure_ascii=False)
        else:
            actual_str = str(actual)
            expect_str = str(expect)

        status = actual_str == expect_str
        if not status:
            print(f'actual result: {actual_str}')
            print(f'expect result: {expect_str}')
            self.result.append(f'actual result: {actual_str}')
            self.result.append(f'expect result: {expect_str}')

        self.result.status = status
