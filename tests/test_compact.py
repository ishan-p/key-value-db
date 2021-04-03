import uuid

from db import Db


class TestMultiCommand(object):

    def test_compact(self):
        db = Db()
        key1 = str(uuid.uuid4())
        key2 = str(uuid.uuid4())
        key3 = str(uuid.uuid4())
        db.set(key3, 10)
        db.compact_begin()
        db.set(key1, "value1")
        db.increment(key2)
        db.set(key1, "value2")
        db.increment_by(key2, 10)
        db.increment_by(key3, 10)
        compact_commands = db.compact_yield()
        assert "SET {key1} value2".format(key1=key1) in compact_commands
        assert "SET {key2} 11".format(key2=key2) in compact_commands
        assert "SET {key3} 20".format(key3=key3) in compact_commands
        assert db.get(key1) is None
        assert db.get(key2) is None
        assert db.get(key3) == 10
        db.delete(key3)

    def test_compact_empty(self):
        db = Db()
        key1 = str(uuid.uuid4())
        key2 = str(uuid.uuid4())
        db.compact_begin()
        db.set(key1, "value1")
        db.increment(key2)
        db.set(key1, "value2")
        db.increment_by(key2, 10)
        db.delete(key1)
        db.delete(key2)
        compact_commands = db.compact_yield()
        assert len(compact_commands) == 0
