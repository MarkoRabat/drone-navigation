import numpy as np
import utils.vector_utils as vutils
from world import WorldObject

# intended way to use this class is camera_object(vec_to_project)
# to project vector to the cameras screen
class Camera(WorldObject):
    """
        Camera class applies perspective projection
        matrix onto objects (points) that are found
        inside of its associated "frustum" - truncated
        piramid. This truncated pyramid represents
        cameras "visible volume".

        Perspective projection consists of
        perspective matrix which squishes the truncated
        piramid (frustum) from sides into a rectangular
        prism (thus applying the perspective transformation)
        and ortographic projection matrix.

        Ortographic projection matrix in turn consists of
        translation matrix which just translates all points
        to which it's applied (in this case all points inside
        of our rectangular prism) to another place and scale
        matrix which scales distances between all points that
        it's applied to (in our case it just "enlarges"
        or "shrinks" our rectangular prism).

        For the sake of simplicity we'll asume that the truncated
        pyramid is aligned along the y-axis => y-axis passes throught
        the center of the smaller base of the truncated pyramid. This
        gives us symetry aroung y-axis and means that distances from
        the left(top) to right(bottom) sides of the base are the same.

        We assume that the center of the coordinate system (relative to camera
        and the truncated pyramid) represents the place where camera is located
        as well as the center of the viewing screen.
    """


    def __init__(self):
        super(Camera, self).__init__()

        self.n = n = 1 # n is distance to the smaller truncated pyramid base along y-axis
        self.f = f = 10 # f is distance to the bigger truncated pyramid base along y-axis

        # f > n -- smaller base of the pyramid is closer to the coordinate center
        if (n > f): n, f = f, n
        if (n == f): raise Exception("Error: camera's view volume = 0 (n == f)")

        # center of the smaller base of the pyramid
        # x and z coordinates have to be 0 in order for the truncated pyramid
        # to be aligned along y-axis as assumed for the sake of symmetry
        near_base_center = (0, n, 0) 

        # truncated pyramids near base dimentions
        self.near_base_width = 40
        self.near_base_height = 40

        self.zoom = 10

        # after perspective projection and translation near base of the pyramid
        # will be scaled so that it fill the whole "viewing screen"
        viewing_screen_width = self.near_base_width * self.zoom
        viewing_screen_height = self.near_base_height * self.zoom

        # coordinatess of the camera object relative to the common frame of reference
        self.camera_position = np.array([0, 0, 0])

        # camera orientation ("the way in which camera looks") - unit vector
        self.camera_orientation = np.array([0, 1, 0])

        # squishes truncated pyramid to rectangular prism
        # thus applying perspective 
        self.perspective_transformation = np.array([
            [n,   0,   0,    0  ],
            [0, f + n, 0, -f * n],
            [0,   0,   n,    0  ],
            [0,   1,   0,    0  ]
        ], dtype=np.float64)

        
        # applies vector addition operation of 
        # -near_base_center vector to all
        # points to in space to which it's applied
        # -- moves near_base_center to coordinate center
        translation_transformation = np.array([
            [1, 0, 0, -near_base_center[0]],
            [0, 1, 0, -near_base_center[1]],
            [0, 0, 1, -near_base_center[2]],
            [0, 0, 0,         1           ]
        ], dtype=np.float64)

        # stretches (squishes) the base of the truncated pyramid
        # in order to take the whole viewing screen
        scale_transformation = np.array([
            [viewing_screen_width / self.near_base_width, 0,                 0,                             0],
            [                0,                           1,                 0,                             0],
            [                0,                           0, viewing_screen_height / self.near_base_height, 0],
            [                0,                           0,                 0,                             1]
        ], dtype=np.float64)

        # first apply translation_transformation then scale_transformation
        # this composes these two operations
        self.ortographic_transformation = np.dot(scale_transformation, translation_transformation)


    # first projectoin operation that should be applied, consists of 2 operations:
    # translation by negative camera position and after that rotation that would
    # align cameras viewing orientation along y-axis if applied to it
    # this function expects input vector to have 4 dimentions, last dim = 1
    def standardize_frame(self, vec_to_project: np.ndarray):
        """
            apply transformations that would align cameras position and orientation
            with the standard frame of reference to all objects that we are projecting
            onto the cameras screen, this is effectively the same as if we switched to
            using cameras frame of reference as the main one, and we see all the objects
            that we want to project as camera "sees" them - thus after applying this
            transformation to the objects we can use standard frame of reference as if
            camera is positioned at the center of it and its viewing orientation is
            alligned along y-axis
        """

        # add -camera_position vector to object (vector) being projected
        translation_transformation = np.array([
            [1, 0, 0, -self.camera_position[0]],
            [0, 1, 0, -self.camera_position[1]],
            [0, 0, 1, -self.camera_position[2]],

            [0, 0, 0,         1           ]
        ], dtype=np.float64)

        # apply translation_transformation to vec_to_project
        translated_vector = np.dot(translation_transformation, vec_to_project)

        # rotate object (vector) being projected by rotation needed to
        # align camera_orientation along y-axis
        rotation_transformation = vutils.rotate_align_matrix(self.camera_orientation, np.array([0, 1, 0, 1]))

        # apply rotation_transformation to translated_vector
        return np.dot(rotation_transformation, translated_vector)

    def set_zoom(self, new_zoom):
        """
            ortographic_transformation that we currently have at the end gives us the screen with width
            and height: (near_base_width * old_zoom, near_base_height * old_zoom), which are the 'old' values,
            and we want to end up with (near_base_width * new_zoom, near_base_height * new_zoom) which are the
            new values; what we therefore need to do is to apply the scaling operation that scales old values
            to the new values to the result of the ortographic_transformation to get screen size that we want
            at the end; but since applying the dot product of two matrices to a vector is the same as applying
            these transformations one after the other, we can just create new ortographic_transformation by
            composing the current one with our new scale transformation, and that is what this function does
        """
        old_viewing_screen_width = self.near_base_width * self.zoom
        old_viewing_screen_height = self.near_base_height * self.zoom

        self.zoom = new_zoom
        new_viewing_screen_width = self.near_base_width * self.zoom
        new_viewing_screen_height = self.near_base_height * self.zoom

        width_scaling_factor = new_viewing_screen_width / old_viewing_screen_width
        height_scaling_factor = new_viewing_screen_height / old_viewing_screen_height

        # scaling matrix
        scale_transformation = np.array([
            [width_scaling_factor,     0,          0,            0],
            [             0,           1,          0,            0],
            [             0,           0, height_scaling_factor, 0],
            [             0,           0,          0,            1]
        ], dtype=np.float64)

        self.ortographic_transformation = np.dot(scale_transformation, self.ortographic_transformation)

    # project standardized frame to screen
    def project_sf(self, vec_to_project: np.ndarray):
        """
            appy perspective and ortographic transformations to a given object (vector),
            this function when applied to an object (vector) from standardized frame
            projects that object onto 2d viewing screen of this (current) camera
            !!! IMPORTANT:
                This function assumes that input vector is inside of standardize_frame,
                    - that it belongs to view volume of the camera, transformed onto sf
        """
        
        # apply perspective transformation:
        perspective_vector = np.dot(self.perspective_transformation, vec_to_project)

        # normalize perspective vector - devide by 4th coordinate in order for it to equal 1
        normalized_perspective_vector = perspective_vector / perspective_vector[3]
        # the magnitude of the normalized vector is different than that of the original input
        # vector, and we want the vector created by perspective transformation to have the
        # same magnitude as the original vector
        normalized_perspective_vector *= vutils.magnitude(vec_to_project) \
            / vutils.magnitude(normalized_perspective_vector)
        normalized_perspective_vector[3] = 1

        # apply ortographic_transformation - vector is projected:
        return np.dot(self.ortographic_transformation, normalized_perspective_vector)

    # intended way to use this class is camera_object(vec_to_project)
    #     - this returns vector projected onto cameras viewing screen
    #     - if y coordinate is negative, that means that the given point
    #           when projected falls outside of viewing screen
    def __call__(self, vec_to_project: np.ndarray):


        if vec_to_project.size < 3:
            raise Exception("Error: only vectors of size 3 or 4 can be projected")

        # make sure that vector has 4 dims, with the last one = 1
        vec_to_project = np.array([
            vec_to_project[0],
            vec_to_project[1],
            vec_to_project[2],
            1
        ])

        vector_in_standardized_frame = self.standardize_frame(vec_to_project)

        # does vec_to_project fall outside of viewing volume
        # if it does we'll flag that by making y negative
        not_visible = vector_in_standardized_frame[1] < self.n \
            or vector_in_standardized_frame[1] > self.f

        # abs(y) must be in [n, f], for now y is always positive
        vector_in_standardized_frame[1] =  min(max(
            vector_in_standardized_frame[1], self.n), self.f)

        # vector projected onto screen
        projected_vector = self.project_sf(vector_in_standardized_frame)

        # not_visible propery indicates whether this point falls outside of
        # viewing screen.
        # if it does fall outside of viewing screen
        # make it fit into it by maximazing | minimazing coordinate values to
        # max_width / 2 or max_height / 2 | -max_width / 2 or max_height / 2 

        viewing_screen_width = self.near_base_width * self.zoom
        viewing_screen_height = self.near_base_height * self.zoom

        if projected_vector[0] > viewing_screen_width // 2:
            projected_vector[0] = viewing_screen_width // 2
            not_visible = True
        elif projected_vector[0] < -viewing_screen_width // 2:
            projected_vector[0] = -viewing_screen_width // 2
            not_visible = True

        if projected_vector[2] > viewing_screen_height // 2:
            projected_vector[2] = viewing_screen_height // 2
            not_visible = True
        elif projected_vector[2] < -viewing_screen_height // 2:
            projected_vector[2] = -viewing_screen_height // 2
            not_visible = True


        # if the point falls outside of viewing screen y is set to
        # negative here; y won't be negative in any other case
        # because of the condition ( (f + n)y_old - fn ) / y_old > 0
        # which is equal to y_old > 0, and since y_old is confined to [n, f]
        # by the previous code, and since n > 0, this condition is always
        # satisfied
        if not_visible: 
            projected_vector[1] = max(projected_vector[1], 1)
            projected_vector[1] *= -1


        return np.delete(projected_vector, 3)







