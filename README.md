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


### TO DOs
- Implement multi command feature
- Add input validation to the service APIs
- Add negative tests
- Implement compact command feature
- Add read lock
- Improve shell cli
- In memory cache

