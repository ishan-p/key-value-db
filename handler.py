from core import DbCore, Record


class DbHandler(object):
    """
    This is a handler interacting between consumer side service class and core db
    """

    def __init__(self):
        self.dbcore = DbCore()
        self.pipe = False
        self.in_memory_db = dict()
        self.delete_keys_pipe = list()

    def create_or_update(self, key, value):
        record = Record(key, value, type(value))
        if self.pipe:
            self.in_memory_db[key] = record
        else:
            file_path = self.dbcore.get_file_path(key)
            self.dbcore.write(file_path, record)
        return record

    def __read(self, key):
        file_path = self.dbcore.get_file_path(key)
        return self.dbcore.read(file_path)

    def read(self, key):
        if self.pipe:
            if key in self.in_memory_db:
                return self.in_memory_db[key]
            else:
                record = self.__read(key)
                self.create_or_update(key, record.value)
        else:
            record = self.__read(key)
        return record

    def delete(self, key):
        if self.pipe:
            self.in_memory_db.pop(key, None)
            self.delete_keys_pipe.append(key)
        else:
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

    def set_pipe(self):
        self.pipe = True

    def execute_pipe(self):
        self.pipe = False
        for key in self.in_memory_db:
            self.create_or_update(key, self.in_memory_db[key].value)
        for key in self.delete_keys_pipe:
            try:
                if key not in self.in_memory_db:
                    self.delete(key)
            except FileNotFoundError:
                continue
        self.in_memory_db = dict()
        self.delete_keys_pipe = list()

    def discard_pipe(self):
        self.in_memory_db = dict()
        self.delete_keys_pipe = list()
        self.pipe = False
