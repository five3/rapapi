import uuid
import time

from .mongotuil import mongo_util
from .replayer import Runner

__all__ = ['RunWithDebug', 'RunWithNormal']


def run(rows, sync):
    runner = Runner(rows)
    runner.start()
    if sync:
        runner.join()

    return runner.results


class RunWithDebug:
    @staticmethod
    def apply_record(rids, sync=True):
        rows = mongo_util.get_record_by_ids(rids)
        return run(rows, sync)

    @staticmethod
    def apply_all(sync=True):
        rows = mongo_util.get_all_record()
        return run(rows, sync)


class RunWithNormal:
    @staticmethod
    def apply_cases(cids, sync=True):
        rows = mongo_util.get_case_by_ids(cids)
        results = run(rows, sync)
        mongo_util.save_result(results)

        return results

    @staticmethod
    def apply_tag(name, sync=True):
        rows = mongo_util.get_case_by_tag(name)
        results = run(rows, sync)
        mongo_util.save_result(results)

        return results

    @staticmethod
    def apply_flow(name, sync=True):
        rows = mongo_util.get_flow_by_name(name)
        results = run(rows, sync)
        mongo_util.save_result(results)

        return results

    @staticmethod
    def apply_set(name, sync=True):
        rows = mongo_util.get_set_by_name(name)
        results = run(rows, sync)
        mongo_util.save_result(results)

        return results


class SaveAsCase:
    @staticmethod
    def save_as_flow(name, condition={}):
        SaveAsCase.save_as_case(flow_name=name, condition=condition)
        SaveAsCase.save_collection(name, "flow")

    @staticmethod
    def save_as_set(name, condition={}):
        SaveAsCase.save_as_case(set_name=name, condition=condition)
        SaveAsCase.save_collection(name, "set")

    @staticmethod
    def save_with_tags(tags, condition={}):
        SaveAsCase.save_as_case(tags=tags, condition=condition)

    @staticmethod
    def save_collection(name, coll_type):
        mongo_util.save_collection({"name": name, "type": coll_type, "created": time.time()})

    @staticmethod
    def save_as_case(flow_name=None, set_name=None, tags=[], condition={}):
        results = mongo_util.get_record_by_condition(condition)
        for result in results:
            result['name'] = result.get('name') or f'api_{uuid.uuid1().hex}'
            result['flow_name'] = flow_name or result.get('flow_name')
            result['set_name'] = set_name or result.get('set_name')
            result['tags'] = tags or result.get('tags')

            mongo_util.save_case(result)


class UpdateCase:
    @staticmethod
    def update_flow(name, condition={}):
        UpdateCase.update_case(flow_name=name, condition=condition)
        UpdateCase.update_collection(name, "flow")

    @staticmethod
    def update_collection(name, coll_type):
        mongo_util.get_first_data_from_coll('collection', {"name": name})
        mongo_util.save_collection({"name": name, "type": coll_type, "created": time.time()})

    @staticmethod
    def update_case(flow_name=None, set_name=None, tags=[], condition={}):
        results = mongo_util.get_case_by_condition(condition)
        for result in results:
            result['name'] = result.get('name') or f'api_{uuid.uuid1().hex}'
            result['flow_name'] = flow_name or result.get('flow_name')
            result['set_name'] = set_name or result.get('set_name')
            result['tags'] = tags or result.get('tags')

            mongo_util.save_case(result)
