from datetime import datetime
from hashlib import md5
import json
import os
import shutil


class Record(object):

    def __init__(self, key, value, dtype, modified_at=None):
        self.key = key
        self.dtype = dtype
        self.value = dtype(value)
        if modified_at:
            self.modified_at = modified_at
        else:
            self.modified_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    def json(self):
        d = dict()
        d['key'] = self.key
        d['dtype'] = self.dtype.__name__
        d['value'] = self.value
        d['modified_at'] = self.modified_at
        return d

    @staticmethod
    def read_record_from_json(obj):
        return Record(
            obj['key'],
            obj['value'],
            eval(obj['dtype']),
            obj['modified_at']
        )


class DbCore(object):

    LEVEL_ONE_BUCKETS = 31
    LEVEL_TWO_BUCKETS = 63
    RECORD_FILE = 'record.json'

    def __init__(self, db_path='./database/'):
        self.db_path = db_path

    @staticmethod
    def hash(key, offset=0):
        h = offset
        for s in list(md5(str(key).encode('utf-8')).hexdigest()):
            h += ord(s)
        return h

    def __map_hash_to_dir_path(self, key):
        dir_1 = str(self.hash(key, 1) % self.LEVEL_ONE_BUCKETS)
        dir_2 = str(self.hash(key, 2) % self.LEVEL_TWO_BUCKETS)
        return os.path.join(dir_1, dir_2)

    def get_file_path(self, key):
        directory = os.path.join(self.db_path, self.__map_hash_to_dir_path(key))
        return os.path.join(directory, key)

