import time
import numpy as np
from camera import Camera
from presenter.pygame_presenter.pyg_screen import PygScreen

pyg_screen1 = PygScreen()
pyg_screen2 = PygScreen()



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

camera1 = Camera()
camera1.camera_position[0] = -5;
camera1.camera_position += np.array([0, 10, -3])
camera2 = Camera()
camera2.camera_position[0] = 5;
camera2.camera_position += np.array([2, -2, -15])

c1line1 = [camera1(line1[0]), camera1(line1[1])]
c1line2 = [camera1(line2[0]), camera1(line2[1])]
c1line3 = [camera1(line3[0]), camera1(line3[1])]
c1line4 = [camera1(line4[0]), camera1(line4[1])]


c2line1 = [camera2(line1[0]), camera2(line1[1])]
c2line2 = [camera2(line2[0]), camera2(line2[1])]
c2line3 = [camera2(line3[0]), camera2(line3[1])]
c2line4 = [camera2(line4[0]), camera2(line4[1])]

for line in [c1line1, c1line2, c1line3, c1line4, c2line1, c2line2, c2line3, c2line4]:
    print(line)
    line[0][0] *= 600/400
    line[0][2] *= -600/400
    line[1][0] *= 600/400
    line[1][2] *= -600/400
    line[0][0] += 600 / 2
    line[0][2] += 600 / 2
    line[1][0] += 600 / 2
    line[1][2] += 600 / 2

print(c1line1)
print(c1line2)
print(c1line3)
print(c1line4)


print(c2line1)
print(c2line2)
print(c2line3)
print(c2line4)

if __name__ == "__main__":
    while True:
        # pyg_screen1.update([(20, 20), (300, 200)])
        pyg_screen1.update([c1line1, c1line2, c1line3, c1line4])

        time.sleep(5)
        # pyg_screen2.update([(200, 200), (100, 400)])
        pyg_screen2.update([c2line1, c2line2, c2line3, c2line4])
        time.sleep(5)
