import sys
sys.path.insert(0, "..")
from utils.vector_utils import *

print()
print("VECTOR_UTILS:")
print("-------------")

print("cross_product tests")

# test[0]
a = np.array([2, 3, 4])
b = np.array([5, 6, 7])
if (cross_product(a, b) == np.array([-3, 6, -3])).all(): print("    test[0] passed")
else: print("    test[0] failed")

# test[1]
a = np.array([2, 3, 4, 1])
b = np.array([5, 6, 7, 1])
if (cross_product(a, b) == np.array([-3, 6, -3, 1])).all(): print("    test[1] passed")
else: print("    test[1] failed")

# test[2]
a = np.array([2, 3, 4])
b = np.array([5, 6, 7, 1])
if (cross_product(a, b) == np.array([-3, 6, -3])).all(): print("    test[2] passed")
else: print("    test[2] failed")

# test[3]
a = np.array([2, 3, 4, 1])
b = np.array([5, 6, 7])
if (cross_product(a, b) == np.array([-3, 6, -3])).all(): print("    test[3] passed")
else: print("    test[3] failed")

# test[4]
a = np.array([2, 3])
b = np.array([5, 6, 7, 1])
emsg = ""
try: cross_product(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function cross_product accepts only arrays of size 3 or 4')":
    print("    test[4] passed")
else: print("    test[4] failed")

# test[5]
a = np.array([2, 3, 4])
b = np.array([5])
emsg = ""
try: cross_product(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function cross_product accepts only arrays of size 3 or 4')":
    print("    test[5] passed")
else: print("    test[5] failed")

print("vector_dot_product tests")

# test[0]
a = np.array([1, 2, 3])
b = np.array([6, 7, 8])
if (vector_dot_product(a, b) == 44): print("    test[0] passed")
else: print("    test[0] failed")

# test[1]
a = np.array([-1, 2, -3, 1])
b = np.array([1, -2, 3])
if (vector_dot_product(a, b) == -14): print("    test[1] passed")
else: print("    test[1] failed")


# test[2]
a = np.array([-1, 2])
b = np.array([1, -2, 3])
emsg = ""
try: vector_dot_product(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function vector_dot_product accepts only arrays of size 3 or 4')":
    print("    test[2] passed")
else: print("    test[2] failed")

# test[3]
a = np.array([-1, 2, -3, 1])
b = np.array([1])
emsg = ""
try: vector_dot_product(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function vector_dot_product accepts only arrays of size 3 or 4')":
    print("    test[3] passed")
else: print("    test[3] failed")

print("magnitude tests")

# test[0]
a = np.array([7, -13, 28.5])
if (magnitude(a) - 32.09750 <= 1e-4): print("    test[0] passed")
else: print("    test[0] failed")

# test[1]
a = np.array([7, -13, 28.5, 1])
if (magnitude(a) - 32.09750 <= 1e-4): print("    test[1] passed")
else: print("    test[1] failed")

# test[2]
a = np.array([0, 0, 0, 1])
if (magnitude(a) <= 1e-15): print("    test[2] passed")
else: print("    test[2] failed")

# test[3]
a = np.array([7, -13])
emsg = ""
try: magnitude(a)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function magnitude accepts only arrays of size 3 or 4')":
    print("    test[3] passed")
else: print("    test[3] failed")


print("angle_between tests")

# test[0]
a = np.array([-1, -3, -5])
b = np.array([-4, -3, -3])
if (angle_between(a, b) - 0.623774666319608 <= 1e-15): print("    test[0] passed")
else: print("    test[0] failed")

# test[1]
a = np.array([-1, -3, -5])
b = np.array([-4, -3, -3, 1])
if (angle_between(a, b) - 0.623774666319608 <= 1e-15): print("    test[1] passed")
else: print("    test[1] failed")

# test[2]
a = np.array([-1, -3])
b = np.array([-4, -3, -3])
emsg = ""
try: angle_between(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function angle_between accepts only arrays of size 3 or 4')":
    print("    test[2] passed")
else: print("    test[2] failed")

# test[3]
a = np.array([-1, -3, -5, 1])
b = np.array([-4])
emsg = ""
try: angle_between(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function angle_between accepts only arrays of size 3 or 4')":
    print("    test[3] passed")
else: print("    test[3] failed")

# test[4]
a = np.array([-1, -3, -5, 1])
b = np.array([0, 0, 0])
if angle_between(a, b) <= 1e-12: print("    test[4] passed")
else: print("    test[4] failed")


print("normalize tests")

# test[0]
a = np.array([17.3, -24.2, 11.1])
if magnitude(normalize(a) - np.array([0.544861, -0.762175, 0.349593])) < 1e-5:
    print("    test[0] passed")
else: print("    test[0] failed")

# test[1]
a = np.array([17.3, -24.2, 11.1, 1])
if magnitude(normalize(a) - np.array([0.544861, -0.762175, 0.349593, 1])) < 1e-5:
    print("    test[1] passed")
else: print("    test[1] failed")

# test[2]
a = np.array([0])
emsg = ""
try: normalize(a)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function normalize accepts only arrays of size 3 or 4')":
    print("    test[2] passed")
else: print("    test[2] failed")

# test[3]
a = np.array([0, 0, 0, 1])
emsg = ""
try: normalize(a)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: vector magnitude is 0')":
    print("    test[3] passed")
else: print("    test[3] failed")


print("rotation_matrix tests")

# test[0]
a = np.array([0, 0, 0, 1])
emsg = ""
try: rotation_matrix(0.3, a)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: rotation axis magnitude is 0')":
    print("    test[0] passed")
else: print("    test[0] failed")

# test[1]
a = np.array([1, 2, 3])
emsg = ""
try: rotation_matrix(0.3, a)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "": print("    test[1] passed")
else: print("    test[1] failed")

# test[2]
a = np.array([1, 2, 3, 1])
emsg = ""
try: rotation_matrix(0.3, a)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "": print("    test[2] passed")
else: print("    test[2] failed")

# test[3]
a = np.array([1, 2])
emsg = ""
try: rotation_matrix(0.3, a)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function rotation_matrix accepts only arrays of size 3 or 4')":
    print("    test[3] passed")
else: print("    test[3] failed")

print("rotate_align_matrix tests")

# test[0]
a = np.array([0, 0, 0, 1])
b = np.array([1, 2, 3])
emsg = ""
try: rotate_align_matrix(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: alignment vector magnitude is 0')":
    print("    test[0] passed")
else: print("    test[0] failed")

# test[1]
a = np.array([1, 2, 3])
b = np.array([0, 0, 0, 1])
emsg = ""
try: rotate_align_matrix(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: alignment vector magnitude is 0')":
    print("    test[1] passed")
else: print("    test[1] failed")

# test[2]
a = np.array([1, 2, 3])
b = np.array([2, 5, 7, 1])
emsg = ""
try: rotate_align_matrix(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "": print("    test[2] passed")
else: print("    test[2] failed")

# test[3]
a = np.array([2, 5, 7, 1])
b = np.array([1, 2, 3])
emsg = ""
try: rotate_align_matrix(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "": print("    test[3] passed")
else: print("    test[3] failed")

# test[4]
a = np.array([2, 5, 7])
b = np.array([1, 2, 3])
emsg = ""
try: rotate_align_matrix(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "": print("    test[4] passed")
else: print("    test[4] failed")

# test[5]
a = np.array([2, 5, 7, 1])
b = np.array([1, 2, 3, 1])
emsg = ""
try: rotate_align_matrix(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "": print("    test[5] passed")
else: print("    test[5] failed")

# test[6]
a = np.array([2])
b = np.array([1, 2, 3, 1])
emsg = ""
try: rotate_align_matrix(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function rotate_align_matrix accepts only arrays of size 3 or 4')":
    print("    test[6] passed")
else: print("    test[6] failed")

# test[7]
a = np.array([2, 5, 7])
b = np.array([1, 2])
emsg = ""
try: rotate_align_matrix(a, b)
except Exception as e: emsg = getattr(e, 'message', repr(e))
if emsg == "Exception('Error: function rotate_align_matrix accepts only arrays of size 3 or 4')":
    print("    test[7] passed")
else: print("    test[7] failed")
