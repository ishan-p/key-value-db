import uuid

from db import Db


class TestOperation(object):

    def test_set(self):
        db = Db()
        key = str(uuid.uuid4())
        value = "test1"
        assert db.set(key, value) == value
        db.delete(key)

    def test_get(self):
        db = Db()
        key = str(uuid.uuid4())
        value = "test1"
        db.set(key, value)
        assert db.get(key) == value
        db.delete(key)

    def test_delete(self):
        db = Db()
        key = str(uuid.uuid4())
        value = "test1"
        db.set(key, value)
        db.delete(key)
        assert db.get(key) is None

    def test_increment(self):
        db = Db()
        key = str(uuid.uuid4())
        db.increment(key)
        assert db.increment(key) == 2
        db.delete(key)

    def test_incremetby(self):
        db = Db()
        key = str(uuid.uuid4())
        db.increment(key)
        assert db.increment_by(key, 21) == 22
        db.delete(key)
