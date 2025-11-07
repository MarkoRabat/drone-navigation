from collections import deque
import utils.vector_utils as vutils
import numpy as np
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
        self.parameters = dict()
    
    def set_parameter(self, param_key, param_value):
        self.parameters[param_key] = param_value
    
    def clear_parameters(self):
        self.parameters = dict()


    def get_oid(self): return self.object_id
    def __call__(self, entity): self.command_function(entity, self.parameters)



AvailableCommands = dict()

def camera_forward(camera, params):
    camera.camera_position += camera.camera_orientation

def camera_beckward(camera, params):
    camera.camera_position -= camera.camera_orientation

def camera_right(camera, params):
    camera.camera_position += camera.camera_normal_orientation

def camera_left(camera, params):
    camera.camera_position -= camera.camera_normal_orientation

def camera_reorient(camera, params):
    if "currx" not in params or "curry" not in params: return
    if "prevx" not in params or "prevy" not in params: return
    prev_pos = np.array([params["prevx"], 1, params["prevy"], 1])
    curr_pos = np.array([params["currx"], 1, params["curry"], 1])
    #print(f"prev_pos: {prev_pos}")
    #print(f"curr_pos: {curr_pos}")
    rotation_angle = vutils.angle_between(
        vutils.normalize(prev_pos), vutils.normalize(curr_pos))
    #rotation_angle = np.log2(rotation_angle)
    #rotation_angle = max(min(rotation_angle, 1.5), 0.2)
    #print(rotation_angle)
    #if rotation_angle < 0.25: return
    rotation_axis = vutils.cross_product(prev_pos, curr_pos)
    #if vutils.magnitude(rotation_axis) < 0.015: return
    rotation_axis = vutils.normalize(rotation_axis)
    print(f"prev_pos: {prev_pos}")
    print(f"curr_pos: {curr_pos}")
    print(rotation_angle)
    print(f"rotation_axis: {rotation_axis}")
    camera.rotate_camera_orientation(rotation_axis, rotation_angle)
    print(f"camera.camera_orientation: {camera.camera_orientation}")

    
AvailableCommands["camera_forward"] = camera_forward
AvailableCommands["camera_beckward"] = camera_beckward
AvailableCommands["camera_right"] = camera_right
AvailableCommands["camera_left"] = camera_left
AvailableCommands["camera_reorient"] = camera_reorient
