from command import Command

# Singleton
class WorldBuilder:
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
#        super(Obj2, self).__init__()


class World:
    def __init__(self): self.elements = dict()

    def __getitem__(self, element_id: int):
        if element_id in self.elements:
            return self.elements[element_id]
        else: return None

    def __iadd__(self, world_object: WorldObject):
        self.elements[world_object.my_wid] = world_object
        return self



"""

    craete a thread inside of each worl that waits on a signal/release
    mutex until there is something in the command queue, and when there
    is, command queue should notify that thread to execute the command

    ??? for some queues where volume is high, maybe use busy wait

    *** for simulation loop use busy wait, as a new thread inside of the world object

signal/release mutex code:

import threading

condition = threading.Condition()
shared_data_ready = False

def waiter():
    print("Waiter: Waiting for signal...")
    with condition:
        while not shared_data_ready:
            condition.wait()  # Wait until notified
        print("Waiter: Got the signal! Proceeding...")

def signaler():
    global shared_data_ready
    with condition:
        print("Signaler: Preparing data...")
        shared_data_ready = True
        condition.notify()  # Send signal to waiting thread
        print("Signaler: Signal sent.")

# Start threads
t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=signaler)

t1.start()
t2.start()

t1.join()
t2.join()
"""




