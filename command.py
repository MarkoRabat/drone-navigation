from collections import deque


class CommandQueue:
    """
        intended usage of a command is:
        for oid in command.get_oids():
            world[oid].exec(command)
                => WorldObjec.exec(command): command(self)
    """

    def __init__(self):
        self.commands = deque()

    def insert_command(self, commad):
        self.commands.append(command)
        if len(self.commands):
            # notify(worlds?)
            # if many: for world in worls: notify(world)
            pass
            

    def delete_command(self, command):
        return self.commands.popleft()


class Command:

    def __init__(self, object_id):
        # id of the object this command should be applied to
        self.object_id = object_id

    def get_oids(self): return [self.object_id]



AvailableCommands = dict()
