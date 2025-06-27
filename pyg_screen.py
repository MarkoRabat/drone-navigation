from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pyg
import numpy as np

pyg.init()
pyg.font.init()
text_font = pyg.font.SysFont("Comic Sans MS", 15)

class PygScreen:

    static_camera_index = 0
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    BG_COLOR = (255, 255, 255)

    def __init__(self):
        PygScreen.static_camera_index += 1
        self.screen_width = self.SCREEN_WIDTH
        self.screen_height = self.SCREEN_HEIGHT
        self.camera_index = PygScreen.static_camera_index
        self.screen = pyg.display.set_mode((self.screen_width, self.screen_height))

    def update(self, data_to_draw):
        pyg.display.set_caption(f"drone simulator {self.camera_index}")
        self.screen.fill(self.BG_COLOR)
        if len(data_to_draw) == 2:
            pyg.draw.line(self.screen, (0, 0, 0), data_to_draw[0], data_to_draw[1])
        pyg.display.flip()

