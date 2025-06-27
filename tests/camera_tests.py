import sys
sys.path.insert(0, "..")
from camera import *

print()
print("CAMERA TESTS:")
print("-------------")

# test[0]:
cam1 = Camera()
cam1.camera_orientation = np.array([7, 7, 7])
cam1.camera_position = np.array([8, 8, 8])
unnormalized_result = cam1.standardize_frame(np.array([15, 15, 15, 1]))
calculated_result = vutils.normalize(unnormalized_result)
correct_rezult = np.array([0, 1, 0, 1])
if vutils.magnitude(correct_rezult - calculated_result) < 1e-15: print("    test[0]: passed")
else: print("    test[0]: failed")
