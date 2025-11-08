import time
import numpy as np
from camera import Camera
from presenter.presenter import Presenter
from presenter.pygame_presenter.pyg_screen import PygScreen
from presenter.pygame_presenter.drawable import DLine, DDrone
from world import WorldBuilder
from command import Command, CommandQueue, AvailableCommands
from command_generator import CommandGeneratorBuilder
from activation import UserInput
from drone_model.drone_model import Drone
import drone_model.physics_engine as pe
import math

pyg_screen1 = PygScreen()
pyg_screen2 = PygScreen()

camera1 = Camera()
camera2 = Camera()

drone = Drone(np.array([0, 4, 0]), 2, camera1)
drone2 = Drone(np.array([12, 4, 12]), 2, camera1)

def print_command5(entity, params):
    print(entity, end=" ")
    print("quit")

command_queue = CommandQueue()

comm1 = Command(AvailableCommands["camera_forward"], 1)
comm2 = Command(AvailableCommands["camera_left"], 1)
comm3 = Command(AvailableCommands["camera_beckward"], 1)
comm4 = Command(AvailableCommands["camera_right"], 1)
comm5 = Command(AvailableCommands["camera_reorient"], 1)
comm6 = Command(print_command5, 1)

def build_world(world):
    world.set_command_queue(command_queue)
    world.start_command_executor()
    user_input1 = UserInput()
    user_input2 = UserInput()
    user_input3 = UserInput()
    user_input4 = UserInput()
    user_input5 = UserInput()
    user_input6 = UserInput()

    def make_command_generator1(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm1) # camera forward
    def make_command_generator2(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm2) # camera left
    def make_command_generator3(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm3) # camera beckward
    def make_command_generator4(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm4) # camera right
    def make_command_generator5(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm5) # camera reorient
    def make_command_generator6(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm6)


    cg1 = CommandGeneratorBuilder().build_with(make_command_generator1)
    cg2 = CommandGeneratorBuilder().build_with(make_command_generator2)
    cg3 = CommandGeneratorBuilder().build_with(make_command_generator3)
    cg4 = CommandGeneratorBuilder().build_with(make_command_generator4)
    cg5 = CommandGeneratorBuilder().build_with(make_command_generator5)
    cg6 = CommandGeneratorBuilder().build_with(make_command_generator6)
    cg1.set_activation(user_input1)
    cg2.set_activation(user_input2)
    cg3.set_activation(user_input3)
    cg4.set_activation(user_input4)
    cg5.set_activation(user_input5)
    cg6.set_activation(user_input6)
    world += camera1
    #camera1.camera_position[0] = -5
    #camera1.camera_position += np.array([2, 2, 2])
    camera1.set_zoom(1)
    world += camera2
    #camera2.camera_position[0] = 5
    #camera2.camera_position += np.array([2, -2, -15])

    pyg_screen1.add_command_activation("forward", user_input1)
    pyg_screen1.add_command_activation("left", user_input2)
    pyg_screen1.add_command_activation("backward", user_input3)
    pyg_screen1.add_command_activation("right", user_input4)
    pyg_screen1.add_command_activation("reorient", user_input5)
    pyg_screen1.add_command_activation("quit", user_input6)
    pyg_screen2.add_command_activation("forward", user_input1)
    pyg_screen2.add_command_activation("left", user_input2)
    pyg_screen2.add_command_activation("backward", user_input3)
    pyg_screen2.add_command_activation("right", user_input4)
    pyg_screen2.add_command_activation("reorient", user_input5)
    pyg_screen2.add_command_activation("quit", user_input6)
    pyg_screen1.start_input_worker()
    pyg_screen2.start_input_worker()
    return world

world = WorldBuilder().build_with(build_world)

point1 = np.array([-16, 4, -16])
point2 = np.array([16, 4, -16])
point3 = np.array([-16, 4, 16])
point4 = np.array([16, 4, 16])

point1[1] = 4
point2[1] = 4
point3[1] = 4
point4[1] = 4

line1 = [point1, point2]
line2 = [point1, point3]
line3 = [point2, point4]
line4 = [point3, point4]

c1line1 = [camera1(line1[0]), camera1(line1[1])]
c1line2 = [camera1(line2[0]), camera1(line2[1])]
c1line3 = [camera1(line3[0]), camera1(line3[1])]
c1line4 = [camera1(line4[0]), camera1(line4[1])]


c2line1 = [camera2(line1[0]), camera2(line1[1])]
c2line2 = [camera2(line2[0]), camera2(line2[1])]
c2line3 = [camera2(line3[0]), camera2(line3[1])]
c2line4 = [camera2(line4[0]), camera2(line4[1])]

camera1_addend = np.array([1, 0, 0])
camera2_addend = np.array([0, 0, 1])
camera1.camera_position += np.array([0, 0, -6])
#camera1.set_camera_orientation(np.array([0, 0, -1]))

#camera1.set_camera_orientation(np.array([0, 0, -1]))



pe.init_gravity_vector_from_unitv(np.array([0, 4.903325, 0]))
print(pe.get_grav_vector())
print("==================")
print(drone.drone_center)
print(drone.motor_coordinates)
#drone.rotate(math.pi / 3, np.array([1, 1, 0]))
print("==================")
print(drone.drone_center)
print(drone.motor_coordinates)
print("==================")
"""
print("==================")
print(drone.drone_center)
print(drone.motor_coordinates)
print("==================")
drone.motor_set_power_percent(0, 0.2)
drone.motor_set_power_percent(1, -0.2)
drone.motor_set_power_percent(2, 0.5)
drone.motor_set_power_percent(3, -0.5)
drone.update()
drone.update()
drone.update()
print("==================")
print(drone.drone_center)
print(drone.motor_coordinates)
print("==================")
"""
#drone.motor_set_power_percent(0, 0.2)
#drone.motor_set_power_percent(1, -0.2)
#drone.motor_set_power_percent(2, 0.2)
#drone.motor_set_power_percent(3, -0.2)
#drone.update()


pid_sleep_time = 10
pid_reset_interval_factor = 100
time_passed = 0
intervals_passed = 0
follow_time = 8
ftime_passed = follow_time
pid_on = True


diff_vec = drone2.drone_center[0:3] - drone.drone_center[0:3]
def update():
    global time_passed
    global intervals_passed
    global pid_on
    global pid_sleep_time
    global ftime_passed
    global diff_vec
    #drone.rotate(-0.03, [0, 1, 0])
    #ground.rotate(-0.03, [0, 1, 0]) # cool ground rotation
    #drone.rotate(-0.15, [1, 0, 0])
    #ground.rotate_ground(-0.03, [0, 1, 0])
    #drone.motor_set_power_percent(0, -0.392)
    #drone.motor_set_power_percent(1, 0.392)
    #drone.motor_set_power_percent(2, -0.392)
    #drone.motor_set_power_percent(3, 0.392)
    if pid_reset_interval_factor:
        drone.pd_params_integral = np.array([0, 0, 0], dtype=float)
    if time_passed == pid_sleep_time:
        if pid_on:
            #drone.pd()
            pass
        time_passed = 0
        intervals_passed += 1
    #drone.move_vector([3, 0])
    drone.nudge_towards_vector([12, 0, 12, 1])
    drone.update()
    if (drone.drone_center[1] > 4.6):
        for i in range(4):
            drone.motor_set_power_percent(i, 0.7)
        time_passed = 8
    
    if (drone.drone_center[1] < 1.5):
        drone.motor_set_power_percent(0, 0.0)
        drone.motor_set_power_percent(1, 0.0)
        drone.motor_set_power_percent(1, 0.0)
        drone.motor_set_power_percent(1, 0.0)
    
    if ftime_passed == follow_time:
        #drone.follow_vector([-1, 0, 0])
        #drone.follow_vector(diff_vec)
        #diff_vec = drone2.drone_center[0:3] - drone.drone_center[0:3]
        drone.nudge_towards_vector([12, 0, 12, 1])
        #drone.move_vector([3, 0])
        #drone.set_stronger([+0.1, +0.1, 0, 0])
        #drone.set_stronger([0, 0, -0.1, -0.1])
        time_passed = 8
        ftime_passed = -2

    time_passed += 1
    ftime_passed += 1
    print("drone: ", drone.drone_center)




pid_sleep_time2 = 10
pid_reset_interval_factor2 = 100
time_passed2 = 0
intervals_passed2 = 0
follow_time2 = 15
pid_on = True
def update2():
    global time_passed2
    global intervals_passed2
    global pid_on
    global pid_sleep_time2
    #drone.rotate(-0.03, [0, 1, 0])
    #ground.rotate(-0.03, [0, 1, 0]) # cool ground rotation
    #drone.rotate(-0.15, [1, 0, 0])
    #ground.rotate_ground(-0.03, [0, 1, 0])
    #drone.motor_set_power_percent(0, -0.392)
    #drone.motor_set_power_percent(1, 0.392)
    #drone.motor_set_power_percent(2, -0.392)
    #drone.motor_set_power_percent(3, 0.392)
    if pid_reset_interval_factor2:
        drone2.pd_params_integral = np.array([0, 0, 0], dtype=float)
    if time_passed2 == pid_sleep_time2:
        if pid_on:
            drone2.pd()
        time_passed2 = 0
        intervals_passed2 += 1
    time_passed2 += 1
    drone2.update()
    if (drone2.drone_center[1] > 4.6):
        drone2.motor_set_power_percent(0, 0.5)
        drone2.motor_set_power_percent(1, 0.5)
        drone2.motor_set_power_percent(2, 0.5)
        drone2.motor_set_power_percent(3, 0.5)
        time_passed2 = 8
    #print("drone2: ", drone2.drone_center)




if __name__ == "__main__":
    while True:
        pyg_screen1([DLine(c1line1), DLine(c1line2), DLine(c1line3), DLine(c1line4), DDrone(drone), DDrone(drone2)])
        #time.sleep(0.02)
        update()
        update2()
        #drone.rotate(math.pi / 12, np.array([0, 0, 1]))
        #pyg_screen2([c2line1, c2line2, c2line3, c2line4])
        #time.sleep(1)

        #camera1.camera_position += camera1_addend * 3
        #camera2.camera_position += camera2_addend * 3
        if camera1.camera_position[0] >= 20:
            camera1_addend = np.array([-1, 0, 0])
        elif camera1.camera_position[0] <= -20:
            camera1_addend = np.array([1, 0, 0])
        if camera2.camera_position[2] >= 20:
            camera2_addend = np.array([0, 0, -1])
        elif camera2.camera_position[2] <= -20:
            camera2_addend = np.array([0, 0, 1])

        c1line1 = [camera1(line1[0]), camera1(line1[1])]
        c1line2 = [camera1(line2[0]), camera1(line2[1])]
        c1line3 = [camera1(line3[0]), camera1(line3[1])]
        c1line4 = [camera1(line4[0]), camera1(line4[1])]

        c2line1 = [camera2(line1[0]), camera2(line1[1])]
        c2line2 = [camera2(line2[0]), camera2(line2[1])]
        c2line3 = [camera2(line3[0]), camera2(line3[1])]
        c2line4 = [camera2(line4[0]), camera2(line4[1])]

        # maybe add server state controller
        #command_queue.delete_command()("Command deleted from queue")
