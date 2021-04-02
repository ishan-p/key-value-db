from db import Db

if __name__ == "__main__":
    supported_commands = ["set",
                          "get",
                          "del",
                          "incr",
                          "incrby"]
    ERROR_MESSAGE = "See usage with help"
    db = Db()
    while True:
        command = input("One2NDB > ")
        commands = command.split(" ")
        operation = commands[0].lower()
        try:
            key = commands[1]
            if operation not in supported_commands:
                print(ERROR_MESSAGE)
            else:
                if operation == "set":
                    try:
                        value = commands[2]
                        db.set(key, value)
                    except IndexError:
                        print(ERROR_MESSAGE)
                elif operation == "get":
                    print(db.get(key))
                elif operation == "del":
                    db.delete(key)
                elif operation == "incr":
                    print(db.increment(key))
                elif operation == "incrby":
                    try:
                        increment_by = commands[2]
                        print(db.increment_by(key, increment_by))
                    except IndexError:
                        print(ERROR_MESSAGE)
        except IndexError:
            print(ERROR_MESSAGE)
