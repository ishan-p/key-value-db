from core import DbCore, Record


class DbHandler(object):

    def __init__(self):
        self.dbcore = DbCore()

    def create_or_update(self, key, value):
        file_path = self.dbcore.get_file_path(key)
        record = Record(key, value, type(value))
        self.dbcore.write(file_path, record)
        return record

    def read(self, key):
        file_path = self.dbcore.get_file_path(key)
        record = self.dbcore.read(file_path)
        return record

    def delete(self, key):
        file_path = self.dbcore.get_file_path(key)
        self.dbcore.delete(file_path)

    def increment_by(self, key, increment_by):
        record = self.read(key)
        new_val = record.value + increment_by
        return self.create_or_update(key, new_val)

    def increment(self, key):
        try:
            record = self.read(key)
            new_val = record.value + 1
            return self.create_or_update(key, new_val)
        except FileNotFoundError:
            return self.create_or_update(key, 1)
