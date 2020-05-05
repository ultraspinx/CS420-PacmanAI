import pygame
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()

    def get_pix_pos(self):
        return (
            vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2 + (self.app.cell_width//2),
                (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2 + (self.app.cell_height//2)))

    def update(self):
        pass

    def draw(self):
        pygame.draw.circle(self.app.screen, RED,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.app.cell_width//2-2)
