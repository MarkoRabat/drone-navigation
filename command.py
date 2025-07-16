from collections import deque
import threading


class CommandQueue:

    MAX_CAPACITY = 500

    def __init__(self):
        self.commands = deque()
        self.max_capacity = CommandQueue.MAX_CAPACITY
        self.lock = threading.Lock() # mutex
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def insert_command(self, command):
        with self.not_full:
            while len(self.commands) >= self.max_capacity:
                self.not_full.wait() # wait for space
            self.commands.append(command)
            self.not_empty.notify() # notify consumers

    def delete_command(self):
        with self.not_empty:
            while not self.commands:
                self.not_empty.wait() # wait for item
            command = self.commands.popleft()
            self.not_full.notify() # notify producers
            return command



class Command:

    def __init__(self, command_function, object_id):
        # id of the object this command should be applied to
        self.command_function = command_function
        self.object_id = object_id

    def get_oid(self): return self.object_id
    def __call__(self, entity): self.command_function(entity)



AvailableCommands = dict()

def camera_forward(camera):
    camera.camera_position += camera.camera_orientation

def camera_beckward(camera):
    camera.camera_position -= camera.camera_orientation
    
AvailableCommands["camera_forward"] = camera_forward
AvailableCommands["camera_beckward"] = camera_beckward
