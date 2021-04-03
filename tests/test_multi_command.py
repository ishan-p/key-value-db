import uuid

from db import Db


class TestMultiCommand(object):

    def test_multi_command_execute(self):
        db = Db()
        key1 = str(uuid.uuid4())
        key2 = str(uuid.uuid4())
        key3 = str(uuid.uuid4())
        db.set(key3, 10)
        db.multi_begin()
        db.set(key1, "value1")
        db.increment(key2)
        db.delete(key1)
        db.set(key1, "value2")
        db.increment_by(key2, 10)
        db.increment_by(key3, 10)
        db.multi_execute()
        assert db.get(key1) == "value2"
        assert db.get(key2) == 11
        assert db.get(key3) == 20
        db.delete(key1)
        db.delete(key2)
        db.delete(key3)

    def test_multi_discard(self):
        db = Db()
        key1 = str(uuid.uuid4())
        key2 = str(uuid.uuid4())
        key3 = str(uuid.uuid4())
        db.set(key3, 10)
        db.multi_begin()
        db.set(key1, "value1")
        db.increment(key2)
        db.set(key1, "value2")
        db.increment_by(key2, 10)
        db.increment_by(key3, 10)
        db.multi_discard()
        assert db.get(key1) is None
        assert db.get(key2) is None
        assert db.get(key3) == 10
        db.delete(key3)
