from command import Command, CommandQueue
import threading
import time

# Singleton
class WorldBuilder:
    """
        def build_world(world):
            build world logic here...
            return world
        world = WorldBuilder().build_with(build_world)
    """
    _instance = None
    def __init__(self): pass
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def build_empty(self): return World()
    def build_with(self, builder_function):
        return builder_function(World())
    def build_from(self, configuration): pass


class WorldObject:
    world_object_id = 0
    def __init__(self):
        WorldObject.world_object_id += 1
        self.my_wid = WorldObject.world_object_id

    def exec(self, command: Command): command(self)

#class Obj2(WorldObject):
#
#    def __init__(self):
#        super().__init__()


class World:
    def __init__(self):
        self.elements = dict()
        self.command_queue = None
        self.executor_stopped = threading.Event()
        self.command_executor = None

    def __getitem__(self, element_id: int):
        if element_id in self.elements:
            return self.elements[element_id]
        else: return None

    def __iadd__(self, world_object: WorldObject):
        self.elements[world_object.my_wid] = world_object
        return self

    def set_command_queue(self, command_queue: CommandQueue):
        self.command_queue = command_queue

    def start_command_executor(self):
        if self.command_queue is None:
            raise Error("world: tried to start executor while command queue is not set")
        if self.command_executor is not None:
            self.stop_command_executor()
        self.command_executor = threading.Thread(target=self.executor_work)
        self.command_executor.start()

    def executor_work(self):
        command_batch_size = 10
        while not self.executor_stopped.is_set():
            for i in range(command_batch_size):
                command = self.command_queue.delete_command()
                if command.get_oid() in self.elements:
                    self.elements[command.get_oid()].exec(command)
            #time.sleep(0.1)

    # thread stopping are not tested
    # potentiali strange situations
    # like thread loocking and memory leaks
    # memory leaks are probably most dangerous
    # and likely threat, dead lock is less likely
    # nothing tested yet, so we don't know
    def stop_command_executor(self):
        self.executor_stopped.set()
        self.command_executor = None

