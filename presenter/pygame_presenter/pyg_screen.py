from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pyg
import numpy as np
from presenter.presenter import Presenter
import time

pyg.init()
pyg.font.init()
text_font = pyg.font.SysFont("Comic Sans MS", 15)

class PygScreen(Presenter):

    static_camera_index = 0
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    BG_COLOR = (255, 255, 255)

    def __init__(self):
        super().__init__()
        PygScreen.static_camera_index += 1
        self.screen_width = self.SCREEN_WIDTH
        self.screen_height = self.SCREEN_HEIGHT
        self.camera_index = PygScreen.static_camera_index
        self.screen = pyg.display.set_mode((self.screen_width, self.screen_height))

    def update_presentation(self, data_to_draw):
        pyg.display.set_caption(f"drone simulator {self.camera_index}")
        self.screen.fill(self.BG_COLOR)
        for line in data_to_draw:
            pyg.draw.line(self.screen, (0, 0, 0), line[0], line[1])
        pyg.display.flip()

    def adjust_data_point(self, data_point):
        # for now data_point is a line
        line = [
            [data_point[0][0] * self.screen_width / 400 + self.screen_width / 2,
            -data_point[0][2] * self.screen_height / 400 + self.screen_height / 2],
            [data_point[1][0] * self.screen_width / 400 + self.screen_width / 2,
            -data_point[1][2] * self.screen_height / 400 + self.screen_height / 2]
        ]
        return line

    def input_worker_work(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT: self.activate_command("quit")
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_w: self.activate_command("forward")
                if event.key == pyg.K_a: self.activate_command("left")
                if event.key == pyg.K_s: self.activate_command("backward")
                if event.key == pyg.K_d: self.activate_command("right")

        """
            elif event.type == pyg.KEYUP:
                if event.key in (pyg.K_w, pyg.K_a, pyg.K_s, pyg.K_d):
                    print(f"{pyg.key.name(event.key).upper()} released")
        """
                
        time.sleep(0.018)
