# O2NDb - A python based key-value db implementation

### Getting Started

Setup a Python 3.6+ virtual environment and install the dependencies.
Usage:
```sh
from db import Db

db_handle = Db()
db_handle.set("key", "value1")
db_handle.get("key")
db_handle.delete("key")

# You can implement counters as follows
db_handle.set("counter", 1)
db_handle.increment("counter")  # Returns 2
db_handle.increment_by("counter", 10)  # Returns 12
```

### Tech Discussions

- Storage
  - Alternative 1 (Implemented): Create a hash table for keys and store each key as an indpendent file located by the hash map
    - Pros:
      - Thread safe
      - Scalable
    - Cons:
      - Suboptimal list keys / scans
      - Slower than in-memory db. But caching can be implemented
  - Alternative 2: Implement in memory database as a python dict
    - Cons:
      -  Creates bottleneck
      -  Potential data loss with application creashing before persisting the db
      -  Cannot implement key level read-write lock
      -  Not thread safe
    - Pros:
      - Faster
      - Better performance for scans
  - Alternative 3: Store paths to the db files for each key in in-memory dict
    - Cons:
      - Slower reads/writes as compared to alternative 1
      - Might create bottleneck
      - Not thread safe
    - Pros:
      - Better scans
      - Easy support to list keys
- Is memory cache required?
- Are optimizations for list / scans required?
- Define error handling


### Multi Command
Usage:
```sh
from db import Db

db_handle = Db()
db_handle.multi_begin()
db_handle.set("key", 1)
db_handle.increment_by("key", 10)
db_handle.multi_execute()  # db_handle.discard() will ignore all multi commands
db_handle.get("key")  # Returns 11
```
Assumptions:
- All commands after multi_begin are executed in memory dict
- discard will ignore all changes and keep persisted db to its original state
- execute will perform all resultant commands (set key from in-memory dict) to the disk, persisting the operations
- Currently implementaion of executing commands to the disk happens sequentially in single thread. But this can easily be scaled by initiating multiple dbCore instances in multi-thread setup
- Reads will happend from the disk if key is absent in-memory
- Current implementation of the multi command is not thread safe


### Compact Command
Assumptions:
- This is a test command to check reduced operations set
- Any command in compact will not be executed
- Internally it uses multi command for reduction and discards all commands on yield

Usage:
```sh
from db import Db

db_handle = Db()
db_handle.compact_begin()
db_handle.set("key", 1)
db_handle.increment_by("key", 10)
compact_commands = db_handle.compact_yield()  # Returns list of reduced commands. ["SET KEY 11"] in this case
```

### TO DOs
- Add input validation to the service APIs
- Add negative tests
- Add read lock
- Improve shell cli
- In memory cache

