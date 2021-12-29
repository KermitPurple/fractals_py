import pygame
import pygame_tools as pgt
from abc import ABC, abstractmethod

class Fractal(ABC):
    '''Abstract class for a fractal'''

    def __init__(
        self,
        window_size: pgt.Point,
        color: pygame.Color,
        screen: pygame.Surface,
    ):
        self.window_size = window_size
        self.center = window_size // 2
        self.color = color
        self.screen = screen

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        '''Draw the fractal'''

class SquareFractal(Fractal):
    '''A square fractal'''

    def draw_square(self, rect: pygame.Rect):
        '''Recursive method to draw squares'''
        pygame.draw.rect(self.screen, self.color, rect, 1)
        new_size = pgt.Point(*rect.size) / 3
        if new_size.x <= 1:
            return
        pos = pgt.Point(*rect.topleft)
        for i in range(3):
            for j in range(3):
                if j != 1 or i != 1:
                    self.draw_square(pygame.Rect(pos + (i, j) * new_size, new_size))

    def draw(self):
        '''Draw the square fractal'''
        size = min(self.window_size)
        rect = pygame.Rect(0, 0, size, size)
        rect.center = self.center
        self.draw_square(rect)

fractals = [SquareFractal]
