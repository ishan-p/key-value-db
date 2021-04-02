from datetime import datetime
import json


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

