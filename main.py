import time
import numpy as np
from camera import Camera
from presenter.presenter import Presenter
from presenter.pygame_presenter.pyg_screen import PygScreen
from world import WorldBuilder
from command import Command, CommandQueue
from command_generator import CommandGeneratorBuilder
from activation import UserInput

pyg_screen1 = PygScreen()
pyg_screen2 = PygScreen()

def print_command1(entity):
    print(entity, end=" ")
    print("forward")

def print_command2(entity):
    print(entity, end=" ")
    print("left")

def print_command3(entity):
    print(entity, end=" ")
    print("backward")

def print_command4(entity):
    print(entity, end=" ")
    print("right")

def print_command5(entity):
    print(entity, end=" ")
    print("quit")

camera1 = Camera()
camera2 = Camera()

command_queue = CommandQueue()

comm1 = Command(print_command1, 1)
comm1("hello from comm1")
comm2 = Command(print_command2, 2)
comm2("hello from comm2")
comm3 = Command(print_command3, 3)
comm3("hello from comm3")
comm4 = Command(print_command4, 4)
comm4("hello from comm4")
comm5 = Command(print_command5, 5)
comm5("hello from comm5")

def build_world(world):
    user_input1 = UserInput()
    user_input2 = UserInput()
    user_input3 = UserInput()
    user_input4 = UserInput()
    user_input5 = UserInput()

    def make_command_generator1(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm1)
    def make_command_generator2(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm2)
    def make_command_generator3(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm3)
    def make_command_generator4(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm4)
    def make_command_generator5(cg):
        cg.set_command_queue(command_queue)
        cg.add_command(comm5)


    cg1 = CommandGeneratorBuilder().build_with(make_command_generator1)
    cg2 = CommandGeneratorBuilder().build_with(make_command_generator2)
    cg3 = CommandGeneratorBuilder().build_with(make_command_generator3)
    cg4 = CommandGeneratorBuilder().build_with(make_command_generator4)
    cg5 = CommandGeneratorBuilder().build_with(make_command_generator5)
    cg1.set_activation(user_input1)
    cg2.set_activation(user_input2)
    cg3.set_activation(user_input3)
    cg4.set_activation(user_input4)
    cg5.set_activation(user_input5)
    world += camera1
    #camera1.camera_position[0] = -5;
    camera1.camera_position += np.array([2, 2, 2])
    #camera1.set_zoom(1)
    world += camera2
    camera2.camera_position[0] = 5;
    camera2.camera_position += np.array([2, -2, -15])

    pyg_screen1.add_command_activation("forward", user_input1)
    pyg_screen1.add_command_activation("left", user_input2)
    pyg_screen1.add_command_activation("backward", user_input3)
    pyg_screen1.add_command_activation("right", user_input4)
    pyg_screen1.add_command_activation("quit", user_input5)
    pyg_screen2.add_command_activation("forward", user_input1)
    pyg_screen2.add_command_activation("left", user_input2)
    pyg_screen2.add_command_activation("backward", user_input3)
    pyg_screen2.add_command_activation("right", user_input4)
    pyg_screen2.add_command_activation("quit", user_input5)
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
if __name__ == "__main__":
    while True:
        pyg_screen1([c1line1, c1line2, c1line3, c1line4])
        time.sleep(0.02)
        #pyg_screen2([c2line1, c2line2, c2line3, c2line4])
        #time.sleep(1)

        camera1.camera_position += camera1_addend * 3
        camera2.camera_position += camera2_addend * 3
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

        command_queue.delete_command()("Command deleted from queue")
