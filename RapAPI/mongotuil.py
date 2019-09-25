#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymongo
from bson import ObjectId

from RapAPI.config import Config


class MongoUtilBase(object):
    def __init__(self, host, port=27017, database='rapapi'):
        self.host = host
        self.port = port
        self.database = database

        self._conn = None
        self._db = None
        self._connect()

    def _connect(self):
        self._conn = pymongo.MongoClient(self.host, self.port)
        self._db = self._conn.get_database(self.database)

    def _disconnect(self):
        self._conn.close()

    def switch_db(self, database):
        self._db = self._conn.get_database(database)

    def get_db_name(self):
        return self._db.name

    def get_data_from_coll(self, name, query={}):
        coll = self._db.get_collection(name)
        return coll.find(query)

    def get_first_data_from_coll(self, name, query={}):
        coll = self._db.get_collection(name)
        return coll.find_one(query)

    def save(self, name, content):
        coll = self._db.get_collection(name)
        return coll.save(content)

    def remove(self, name, query={}):
        coll = self._db.get_collection(name)
        return coll.remove(query)


class MongoUtil(MongoUtilBase):
    # record
    def get_record_by_ids(self, aids):
        ids = [ObjectId(aid) for aid in aids]
        return self.get_data_from_coll('record', {'_id': {'in': ids}}).sort('request_no', pymongo.ASCENDING)

    def get_record_by_condition(self, condition={}):
        return self.get_data_from_coll('record', condition).sort('request_no', pymongo.ASCENDING)

    def get_all_record(self):
        return self.get_data_from_coll('record').sort('request_no', pymongo.ASCENDING)

    def save_record(self, content):
        return self.save('record', content)

    def clear_record(self):
        return self.remove('record')

    # case
    def get_case_by_ids(self, cids):
        ids = [ObjectId(cid) for cid in cids]
        return self.get_data_from_coll('case', {'_id': {'in': ids}}).sort('request_no', pymongo.ASCENDING)

    def get_case_by_condition(self, condition={}):
        return self.get_data_from_coll('case', condition).sort('request_no', pymongo.ASCENDING)

    def get_case_by_tag(self, name):
        return self.get_data_from_coll('case', {'tags': name}).sort('request_no', pymongo.ASCENDING)

    def get_flow_by_name(self, name):
        return self.get_data_from_coll('case', {'flow_name': name}).sort('request_no', pymongo.ASCENDING)

    def get_set_by_name(self, name):
        return self.get_data_from_coll('case', {'set_name': name}).sort('request_no', pymongo.ASCENDING)

    def save_case(self, content):
        return self.save('case', content)

    def save_all_case(self, contents):
        for content in contents:
            self.save('case', content)

    # collection
    def save_collection(self, content):
        return self.save('collection', content)

    def get_all_collection(self):
        return self.get_data_from_coll('collection').sort('created', pymongo.DESCENDING)

    # result
    def save_result(self, results):
        for result in results:
            self.save('result', result.output)

    # config
    def get_config(self):
        return self.get_first_data_from_coll('config')


mongo_util = MongoUtil(Config.MONGO_HOST)
