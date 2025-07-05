import time
import numpy as np
from camera import Camera
from presenter.pygame_presenter.pyg_screen import PygScreen
from world import WorldBuilder

pyg_screen1 = PygScreen()
pyg_screen2 = PygScreen()


camera1 = Camera()
camera2 = Camera()

def build_world(world):
    world += camera1
    #camera1.camera_position[0] = -5;
    camera1.camera_position += np.array([2, 2, 2])
    #camera1.set_zoom(1)
    world += camera2
    camera2.camera_position[0] = 5;
    camera2.camera_position += np.array([2, -2, -15])
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
        time.sleep(1)
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
