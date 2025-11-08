import pygame as pyg
import drone_model.physics_engine as pe
import numpy as np

class Drawable:

    def __init__(self, data):
        self.data = data
        self.presenter = None

    def draw(self): pass
    def adjust(self): return None
    def set_presenter(self, p): self.presenter = p


class DLine(Drawable):

    def draw(self):
        pyg.draw.line(self.presenter.screen, (0, 0, 0), self.data[0], self.data[1])
    
    def adjust(self):
        if self.data[0][1] < 0 or self.data[1][1] < 0:
            dl = DLine([[0, 0], [0, 0]])
            dl.set_presenter(self.presenter)
            return dl
        line = [
            [self.data[0][0] * self.presenter.screen_width / 400 + self.presenter.screen_width / 2,
            -self.data[0][2] * self.presenter.screen_height / 400 + self.presenter.screen_height / 2],
            [self.data[1][0] * self.presenter.screen_width / 400 + self.presenter.screen_width / 2,
            -self.data[1][2] * self.presenter.screen_height / 400 + self.presenter.screen_height / 2]
        ]
        dl = DLine(line)
        dl.set_presenter(self.presenter)
        return dl

class DDrone(Drawable):

    def draw(self):
        body_width = 2
        motor_point_size = 1
        motor_width = 1

        drone = self.data["drone"]
        motors = self.data["motors"]
        drone_center = self.data["drone_center"]
        propellers = self.data["propellers"]
        propeller_centers = self.data["propeller_ceters"]
        mmax = self.data["mmax"]

        if drone_center[2] < 0: return

        if drone.thrust_vectors is not None:
            pyg.draw.line(self.presenter.screen, (255, 0, 0), tuple(self.data["gravity_force_begin"][0:2]), tuple(self.data["gravity_force_end"][0:2]), 3)
        for i in range(3, -1, -1):
            motor_point_scaling = motor_point_size * motors[i][2] / mmax
            if motors[i][2] > 0:
                pyg.draw.circle(self.presenter.screen, drone.motor_color, (motors[i][0], motors[i][1]), motor_point_scaling, motor_width)
            for j in range(len(propellers[i])):
                if propellers[i][j][2] < 0: continue
                pyg.draw.circle(self.presenter.screen, drone.motor_color, (propellers[i][j][0], propellers[i][j][1]), motor_point_scaling, motor_width)
            for j in range(4):
                if propeller_centers[i][2] < 0: continue
                pyg.draw.line(self.presenter.screen, drone.propeller_color, tuple(propeller_centers[i][0:2]), tuple(propellers[i][j][0:2]), 4)
                if drone.thrust_vectors is not None:
                    pyg.draw.line(self.presenter.screen, (0, 255, 0), tuple(self.data["thrust_force_begin"][i][0:2]), tuple(self.data["thrust_force_end"][i][0:2]), 3)
            pyg.draw.line(self.presenter.screen, drone.body_color, tuple(motors[i][0:2]), drone_center[0:2], width=body_width)

    
    def adjust(self):
        if self.data.pr is None: raise Exception("camera to project onto not supplied to drone")
        thrust_scaling_factor = 0.0002
        gravity_scaling_factor = 0.025
        motors = self.data.motor_coordinates[self.data.motor_coordinates[:, 2].argsort()][:, :-1]
        drone_center = np.copy(self.data.drone_center)

        new_ddrone = {
            "drone": self.data,
        }

        if self.data.thrust_vectors is not None:
            thrust_force_vectors = np.insert(thrust_scaling_factor * self.data.thrust_vectors, 3, np.full(shape=4, fill_value=0, dtype=float), axis=1)
            thrust_force_begin = self.data.propeller_centers + 0.2 * pe.normalize_vector(thrust_force_vectors[0])
            thrust_force_end = self.data.propeller_centers + thrust_force_vectors
            thrust_force_begin = thrust_force_begin[self.data.propeller_centers[:, 2].argsort()][:, :-1]
            thrust_force_end = thrust_force_end[self.data.propeller_centers[:, 2].argsort()][:, :-1]
            gravity_force_vector = np.insert(gravity_scaling_factor * self.data.gravity_vector, 3, np.array([1]), axis=0)
            gravity_force_begin = drone_center + 2 * pe.normalize_vector(gravity_force_vector)
            gravity_force_end = drone_center + gravity_force_vector
        
        propeller_centers = self.data.propeller_centers[self.data.propeller_centers[:, 2].argsort()][:, :-1]

        pvals = np.array([
            [self.data.propellers[0, :, 2].min(), 0],
            [self.data.propellers[1, :, 2].min(), 1],
            [self.data.propellers[2, :, 2].min(), 2],
            [self.data.propellers[3, :, 2].min(), 3]
        ])
        propellers = self.data.propellers[pvals[pvals[:, 0].argsort()][:, 1].astype(int)]
        cols_to_remove = np.array([False, False, False, True])
        propellers = propellers[:, :, ~cols_to_remove] # remove 4th column in each entry

        for i in range(4):
            motors[i] = self.data.pr(motors[i])
            propeller_centers[i] = self.map_onto_screen(self.data.pr(propeller_centers[i]))
            if self.data.thrust_vectors is not None:
                thrust_force_begin[i] = self.map_onto_screen(self.data.pr(thrust_force_begin[i]))
                thrust_force_end[i] = self.map_onto_screen(self.data.pr(thrust_force_end[i]))
            for j in range(len(propellers[i])):
                propellers[i][j] = self.map_onto_screen(self.data.pr(propellers[i][j]))
        drone_center = self.data.pr(drone_center)
        if self.data.thrust_vectors is not None:
            gravity_force_begin = self.data.pr(gravity_force_begin)
            gravity_force_end = self.data.pr(gravity_force_end)
            new_ddrone["thrust_force_begin"] = thrust_force_begin
            new_ddrone["thrust_force_end"] = thrust_force_end
            new_ddrone["gravity_force_begin"] = gravity_force_begin
            new_ddrone["gravity_force_end"] = gravity_force_end

        mmax = motors[:, 2].max()
        for i in range(4):
            motors[i] = self.map_onto_screen(motors[i])

        new_ddrone["motors"] = motors
        new_ddrone["drone_center"] = self.map_onto_screen(drone_center)
        new_ddrone["propellers"] = propellers
        new_ddrone["propeller_ceters"] = propeller_centers
        new_ddrone["mmax"] = mmax

        dd = DDrone(new_ddrone)
        dd.set_presenter(self.presenter)
        return dd
    
    def map_onto_screen(self, dp): # add 1 more dim for numpy array dim alignment
        #if dp[1] < 0 : return [0, 0, 0]
        mapped = [dp[0] * self.presenter.screen_width / 400 + self.presenter.screen_width / 2,
            -dp[2] * self.presenter.screen_height / 400 + self.presenter.screen_height / 2, 0]
        if dp[1] < 0: mapped[2] = -1
        return mapped
        
