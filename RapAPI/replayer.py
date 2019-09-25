import time
import requests
import threading
import threadpool
import logging

from .result import Result
from .validator import Validator
from .constants import CollectionType
from .config import Config

__all__ = ['Runner']

requests.packages.urllib3.disable_warnings()


class Runner(threading.Thread):
    def __init__(self, records, collection_type=CollectionType.FLOW):
        super().__init__()
        self.records = records
        self.collection_type = collection_type
        self._results = []

    def run(self):
        replay_args = []
        for row in self.records:
            result = Result(row['_id'])
            result.url = row['request_data']['url']
            result.append(f'Run collection as [{self.collection_type}]')

            validator = Validator(row.get('verify_type', 'json'), result)
            self._results.append(result)

            if self.collection_type == CollectionType.FLOW:     # 以Flow的方式执行API集合
                self.replay(row, validator)
            else:
                replay_args.append((row, validator))

        if self.collection_type != CollectionType.FLOW:         # 非Flow方式以多线程并发形式执行API集合
            pool = threadpool.ThreadPool(Config.THREAD_POOL_MAX_NUM)
            reqs = threadpool.makeRequests(self.replay, replay_args)
            [pool.putRequest(req) for req in reqs]
            pool.wait()

    def wait(self):
        flag = False
        while not flag:
            time.sleep(1)
            flag = all([result.is_finished for result in self._results])

    @property
    def results(self):
        return self._results

    @staticmethod
    def replay(row, validator=None):
        request_data = row['request_data']
        response_data = row['response_data']
        response_data.pop('text')
        exclude = row.get('exclude')
        not_empty = row.get('not_empty')

        try:
            headers = request_data['headers']
            data = request_data['content']
            rep = requests.request(request_data['method'].lower(), request_data['url'],
                                   data=data, headers=headers, allow_redirects=True, verify=False)

            actual = {
                'status_code': rep.status_code,
                'reason': rep.reason,
                'headers': dict(rep.headers),
                'content': rep.content
            }

            if validator:
                validator.verify(actual, response_data, not_empty=not_empty, exclude=exclude)

            return actual

        except Exception as e:
            reason = f"<Replay> HTTP request ERROR. {e}"
            validator.result.append(reason)
            logging.exception(e)
            raise ValueError(reason)
        finally:
            if validator:
                validator.result.is_finished = True
