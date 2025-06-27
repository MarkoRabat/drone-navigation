import numpy as np
import utils.vector_utils as vutils

class Camera:
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

        n = 10 # n is distance to the smaller truncated pyramid base along y-axis
        f = 20 # f is distance to the bigger truncated pyramid base along y-axis

        # f > n -- smaller base of the pyramid is closer to the coordinate center
        if (n > f): n, f = f, n
        if (n == f): raise Exception("Error: camera's view volume = 0 (n == f)")

        # center of the smaller base of the pyramid
        # x and z coordinates have to be 0 in order for the truncated pyramid
        # to be aligned along y-axis as assumed for the sake of symmetry
        near_base_center = (0, n, 0) 

        # truncated pyramids near base dimentions
        near_base_width = 10
        near_base_height = 5

        # after perspective projection and translation near base of the pyramid
        # will be scaled so that it fill the whole "viewing screen"
        self.viewing_screen_width = 20
        self.viewing_screen_height = 30

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
            [viewing_screen_width / near_base_width, 0,                 0,                        0],
            [                0,                      1,                 0,                        0],
            [                0,                      0, viewing_screen_height / near_base_height, 0],
            [                0,                      0,                 0,                        1]
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

        # apply ortographic_transformation - vector is projected:
        return np.dot(self.ortographic_transformation, normalized_perspective_vector)

    # intended way to use this class is camera_object(vec_to_project)
    #     - this should return vector projected to cameras viewing screen
    def __call__(self, vec_to_project: np.ndarray):

        if vec_to_project.size < 3:
            raise Exception("Error: only vectors of size 3 or 4 can be projected")

        # make sure that vector has 4 dims, whil the last one = 1
        vec_to_project = np.array([
            vec_to_project[0],
            vec_to_project[1],
            vec_to_project[2],
            1
        ])

        vector_in_standardized_frame = self.standardize_frame(vec_to_project)

        # vector projected onto screen
        projected_vector = self.project_sf(vector_in_standardized_frame)

        # assing propery indicating whether this point falls inside of
        # viewing screen and if it does fall outside of viewing screen
        # make it fit into it by maximazing | minimazing coordinate values to
        # max_width / 2 or max_height / 2 | -max_width / 2 or max_height / 2 

        projected_vector.isinside_viewing_screen = True

        if projected_vector[0] > self.viewing_screen_width // 2:
            projected_vector[0] = self.viewing_screen_width // 2
            projected_vector.isinside_viewing_screen = False
        elif projected_vector[0] < -self.viewing_screen_width // 2
            projected_vector[0] = -self.viewing_screen_width // 2
            projected_vector.isinside_viewing_screen = False

        if projected_vector[2] > self.viewing_screen_height // 2:
            projected_vector[2] = self.viewing_screen_height // 2
            projected_vector.isinside_viewing_screen = False
        elif projected_vector[2] < -self.viewing_screen_height // 2:
            projected_vector[2] = -self.viewing_screen_height // 2
            projected_vector.isinside_viewing_screen = False

        return projected_vector






