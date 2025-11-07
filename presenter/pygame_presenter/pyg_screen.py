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
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 1600
    BG_COLOR = (255, 255, 255)

    def __init__(self):
        super().__init__()
        PygScreen.static_camera_index += 1
        self.screen_width = self.SCREEN_WIDTH
        self.screen_height = self.SCREEN_HEIGHT
        self.camera_index = PygScreen.static_camera_index
        self.screen = pyg.display.set_mode((self.screen_width, self.screen_height))
        self.prev_mouse_pos = None

    def update_presentation(self, data_to_draw):
        pyg.display.set_caption(f"drone simulator {self.camera_index}")
        self.screen.fill(self.BG_COLOR)
        for d2d in data_to_draw: d2d.draw()
        pyg.display.flip()

    def adjust_data_point(self, data_point):
        data_point.set_presenter(self)
        return data_point.adjust()

    def input_worker_work(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT: self.activate_command("quit")
            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_w: self.activate_command("forward")
                if event.key == pyg.K_a: self.activate_command("left")
                if event.key == pyg.K_s: self.activate_command("backward")
                if event.key == pyg.K_d: self.activate_command("right")
            elif event.type == pyg.MOUSEMOTION:
                if self.prev_mouse_pos is not None and pyg.mouse.get_pressed()[0]:
                    if ((self.prev_mouse_pos[0] - event.pos[0]) ** 2 \
                        + (self.prev_mouse_pos[1] - event.pos[1]) ** 2) ** 0.5 \
                        < 0.05: return
                    self.activate_command("reorient", [
                        ["currx", event.pos[0] / self.SCREEN_WIDTH],
                        ["curry", (self.SCREEN_HEIGHT - event.pos[1]) / self.SCREEN_HEIGHT],
                        ["prevx", self.prev_mouse_pos[0] / self.SCREEN_WIDTH],
                        ["prevy", (self.SCREEN_HEIGHT - self.prev_mouse_pos[1]) / self.SCREEN_HEIGHT]
                    ])
                self.prev_mouse_pos = event.pos

        """
            elif event.type == pyg.KEYUP:
                if event.key in (pyg.K_w, pyg.K_a, pyg.K_s, pyg.K_d):
                    print(f"{pyg.key.name(event.key).upper()} released")
        """
                
        time.sleep(0.018)
