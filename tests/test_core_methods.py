import uuid

from core import DbCore, Record

class TestCore(object):

    def test_if_same_hash_map_is_generated_for_same_keys(self):
        key = str(uuid.uuid4())
        dbcore = DbCore()
        assert dbcore.get_file_path(key) == dbcore.get_file_path(key)

    def test_read_write(self):
        key = str(uuid.uuid4())
        value = "test"
        dbcore = DbCore()
        record = Record(key, value, type(value))
        folder_path = dbcore.get_file_path(key)
        dbcore.write(folder_path, record)
        assert dbcore.read(folder_path).value == value
        dbcore.delete(folder_path)

    def test_delete(self):
        key = str(uuid.uuid4())
        value = "test"
        dbcore = DbCore()
        record = Record(key, value, type(value))
        folder_path = dbcore.get_file_path(key)
        dbcore.write(folder_path, record)
        dbcore.delete(folder_path)
        try:
            dbcore.read(folder_path)
        except FileNotFoundError:
            assert True
