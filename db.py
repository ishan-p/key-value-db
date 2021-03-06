from handler import DbHandler


class Db(object):
    """
    This is the service class providing API to our db consumers
    """

    def __init__(self):
        self.handle = DbHandler()

    def set(self, key, value):
        record = self.handle.create_or_update(key, value)
        return record.value

    def get(self, key):
        try:
            record = self.handle.read(key)
            return record.value
        except FileNotFoundError:
            return None

    def delete(self, key):
        self.handle.delete(key)

    def increment(self, key):
        record = self.handle.increment(key)
        return record.value

    def increment_by(self, key, increment_by):
        try:
            record = self.handle.increment_by(key, increment_by)
            return record.value
        except FileNotFoundError:
            return None

    def multi_begin(self):
        self.handle.set_pipe()

    def multi_execute(self):
        self.handle.execute_pipe()

    def multi_discard(self):
        self.handle.discard_pipe()

    def compact_begin(self):
        if self.handle.pipe:
            raise Exception("Compact cannot be used in multi command mode")
        else:
            self.handle.set_pipe()

    def compact_yield(self):
        compact_commands = self.handle.compact()
        self.handle.discard_pipe()
        for command in compact_commands:
            print(command)
        return compact_commands
