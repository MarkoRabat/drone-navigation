from collections import deque


class CommandQueue:
    """
        intended usage of a command is:
        world[command.get_oid()].exec(command)
            => WorldObjec.exec(command): command(self)
    """

    def __init__(self):
        self.commands = deque()

    def insert_commad(self, commad):
        self.commands.append(command)

    def delete_command(self, command):
        return self.commands.popleft()


class Command:

    def __init__(self, object_id):
        # id of the object this command should be applied to
        self.object_id = object_id

    def get_oid(self): return self.object_id

