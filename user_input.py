from collections import deque


class CommandQueue:

    def __init__(self):
        self.user_commands = deque()

    def insert_commad(self, commad):
        self.user_commands.append(command)

    def delete_command(self, command):
        return self.user_commands.popleft()

class UserCommand:

    def __init__(self, object_id):
        # id of the object this command should be applied to
        self.object_id = object_id

