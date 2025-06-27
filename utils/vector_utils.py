import numpy as np

def cross_product(u : np.ndarray, v : np.ndarray):
    if u.size >= 4 and v.size >= 4:
        return np.array([
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0],
            1
        ], dtype=float)
    elif u.size >= 3 and v.size >= 3:
        return np.array([
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]
        ], dtype=float)
    raise Exception("Error: function cross_product accepts only arrays of size 3 or 4")

def vector_dot_product(u : np.ndarray, v : np.ndarray):
    if u.size < 3 or v.size < 3:
        raise Exception("Error: function vector_dot_product accepts only arrays of size 3 or 4")
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]

# it's done this way because our vectors can either have 3 dimentions or
# they can have 4 dimentions where last coordinate is 1, in the latter case 
# we don't want to include the 4th coordinate in magnitude calculation
def magnitude(vec : np.ndarray):
    if vec.size < 3:
        raise Exception("Error: function magnitude accepts only arrays of size 3 or 4")
    return np.sqrt(
        vec[0] * vec[0]
      + vec[1] * vec[1]
      + vec[2] * vec[2]
    )

# returns angle between vectors u and v in radians
def angle_between(u : np.ndarray, v : np.ndarray):
    if u.size < 3 or v.size < 3:
        raise Exception("Error: function angle_between accepts only arrays of size 3 or 4")
    if magnitude(u) == 0 or magnitude(v) == 0: return 0
    return np.arccos(vector_dot_product(u, v) / magnitude(u) / magnitude(v))

def normalize(vec : np.ndarray):
    if vec.size < 3:
        raise Exception("Error: function normalize accepts only arrays of size 3 or 4")
    if magnitude(vec) < 1e-15: raise Exception("Error: vector magnitude is 0")
    vec = vec / magnitude(vec)
    if vec.size >= 4: vec[3] = 1
    return vec

# return transformation matrix that rotates vectors around given axis (as a [unit] vector)
# angle degrees (in radians, or convert degrees to radians), this matrix rotates space
# counterclockwise (around the given [unit] vector)
def rotation_matrix(angle : float, unit_vector : np.ndarray, degrees=False):
    if unit_vector.size < 3:
        raise Exception("Error: function rotation_matrix accepts only arrays of size 3 or 4")
    if magnitude(unit_vector) < 1e-15: raise Exception("Error: rotation axis magnitude is 0")
    unit_vector = normalize(unit_vector)
    if degrees: angle = angle * np.pi / 180
    return np.array([
        [
            np.cos(angle) + unit_vector[0] * unit_vector[0] * (1 - np.cos(angle)),
            unit_vector[0] * unit_vector[1] * (1 - np.cos(angle)) - unit_vector[2] * np.sin(angle),
            unit_vector[0] * unit_vector[2] * (1 - np.cos(angle)) + unit_vector[1] * np.sin(angle),
            0
        ],
        [
            unit_vector[1] * unit_vector[0] * (1 - np.cos(angle)) + unit_vector[2] * np.sin(angle),
            np.cos(angle) + unit_vector[1] * unit_vector[1] * (1 - np.cos(angle)),
            unit_vector[1] * unit_vector[2] * (1 - np.cos(angle)) - unit_vector[0] * np.sin(angle),
            0
        ],
        [
            unit_vector[2] * unit_vector[0] * (1 - np.cos(angle)) - unit_vector[1] * np.sin(angle),
            unit_vector[2] * unit_vector[1] * (1 - np.cos(angle)) + unit_vector[0] * np.sin(angle),
            np.cos(angle) + unit_vector[2] * unit_vector[2] * (1 - np.cos(angle)),
            0
        ],
        [
            0,
            0,
            0,
            1
        ]
    ])

# a function that returns matrix transformation that when applied to
# vector v1 aligns that vector to the vector v2 (if v1 and v2 have the
# same magnitude, applying this transformation to v1 produces v2)
def rotate_align_matrix(u : np.ndarray, v : np.ndarray):
    if u.size < 3 or v.size < 3:
        raise Exception("Error: function rotate_align_matrix accepts only arrays of size 3 or 4")
    if magnitude(u) < 1e-15 or magnitude(v) < 1e-15:
        raise Exception("Error: alignment vector magnitude is 0")

    # we normalize v1 and v2 in case they are not unit vectors
    u = normalize(u); v = normalize(v)
    axis = cross_product(u, v)

    cosA = vector_dot_product(u, v)
    k = 1.0 / (1.0 + cosA)

    return np.array([
        [
            axis[0] * axis[0] * k + cosA,
            axis[1] * axis[0] * k - axis[2], 
            axis[2] * axis[0] * k + axis[1],
            0
        ],
        [
            axis[0] * axis[1] * k + axis[2],  
            axis[1] * axis[1] * k + cosA,      
            axis[2] * axis[1] * k - axis[0],
            0
        ],
        [
            axis[0] * axis[2] * k - axis[1],  
            axis[1] * axis[2] * k + axis[0],  
            axis[2] * axis[2] * k + cosA,
            0
        ],
        [
            0,
            0,
            0,
            1
        ]
    ])



