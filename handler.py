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

