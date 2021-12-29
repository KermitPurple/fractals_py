#!/usr/bin/env python3

import pygame
import pygame_tools as pgt
from fractals import fractals

class FractalsSim(pgt.GameScreen):
    '''
    A fractal simulator
    '''

    BG = pygame.Color('black')
    FG = pygame.Color('WHITE')

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Fractals')
        size = pgt.Point(1400, 750)
        super().__init__(pygame.display.set_mode(size), size)
        self.fractals = list(map(lambda x: x(self.window_size, self.FG, self.screen), fractals))
        self.fractal_index = 0
        self.fractal_len = len(fractals)
        self.fractal = self.fractals[self.fractal_index]

    def update(self):
        self.screen.fill(self.BG)
        self.fractal.draw()

    def key_down(self, event: pygame.event.Event):
        unicode = event.unicode.lower()
        match unicode:
            case ' ':
                self.fractal_index += 1
                if self.fractal_index >= self.fractal_len:
                    self.fractal_index = 0
                self.fractal = self.fractals[self.fractal_index]

def main():
    '''Driver Code'''
    FractalsSim().run()

if __name__ == "__main__":
    main()
