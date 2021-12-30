import pygame, math
import pygame_tools as pgt
from abc import ABC, abstractmethod
from typing import List
from itertools import chain

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
    def draw(self):
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

class SierpinskiTriangle(Fractal):
    '''The Sierpinski Triangle fractal'''

    @staticmethod
    def get_midpoint(a: pgt.Point, b: pgt.Point) -> pgt.Point:
        '''
        get the midpoint of 2  points
        '''
        return (a + b) / 2

    @staticmethod
    def get_midpoints(points: List[pgt.Point]) -> List[pgt.Point]:
        '''
        get the midpoints of all adjacent points in this list
        '''
        if len(points) != 3:
            raise ValueError('Triangles have Exactly 3 points man')
        result = []
        prev = points[-1]
        for point in points:
            result.append((prev + point) / 2)
            prev = point
        return result

    def draw_triangle(self, points: List[pgt.Point]):
        '''Recursive method for drawing triangles'''
        if pgt.Point.distance(points[1], points[2]) <= 1:
            return
        midpoints = self.get_midpoints(points)
        pygame.draw.lines(
            self.screen,
            self.color,
            True,
            midpoints,
        )
        self.draw_triangle([
            points[0],
            self.get_midpoint(points[0], points[1]),
            self.get_midpoint(points[0], points[2]),
        ])
        self.draw_triangle([
            points[1],
            self.get_midpoint(points[1], points[0]),
            self.get_midpoint(points[1], points[2]),
        ])
        self.draw_triangle([
            points[2],
            self.get_midpoint(points[2], points[1]),
            self.get_midpoint(points[2], points[0]),
        ])

    def draw(self):
        '''Draw the sierpinski triangle'''
        points = [
            self.center * (1, 0),
            self.window_size / (3, 1) - (0, 1),
            self.window_size * (2 / 3, 1) - (0, 1)
        ]
        pygame.draw.lines(
            self.screen,
            self.color,
            True,
            points
        )
        self.draw_triangle(points)

class FractalTree(Fractal):
    '''The Fractal Tree'''

    def draw_tree(self, pos: pgt.Point, length: int, theta: float = math.pi / 2):
        '''Recursive method to draw tree'''
        new_pos = pos - pgt.Point(math.cos(theta), math.sin(theta)) * length
        pygame.draw.line(
            self.screen,
            self.color,
            pos,
            new_pos
        )
        length //= 2
        if length <= 1:
            return
        self.draw_tree(
            new_pos,
            length,
            math.pi / 4
        )
        self.draw_tree(
            new_pos,
            length,
            3 * math.pi / 4
        )

    def draw(self):
        '''Draw the entire tree'''
        self.draw_tree(
            self.window_size // (2, 1),
            self.window_size.y / 3,
        )

class HilbertCurve(Fractal):
    '''A curving fractal'''

    @staticmethod
    def rotate_around(pos: pgt.Point, origin: pgt.Point, theta: float) -> pgt.Point:
        x, y = pos - origin
        return pgt.Point(
            x * math.cos(theta) - y * math.sin(theta),
            y * math.cos(theta) + x * math.sin(theta)
        ) + origin

    def draw_curve(self, points: List[pgt.Point]):
        '''Recursive method for drawing curve'''
        dist = pgt.Point.distance(*points[:2])
        if dist <= 5:
            pygame.draw.lines(
                self.screen,
                self.color,
                False,
                points,
                1
            )
            return
        new_dist = dist // 4
        origin = self.center
        scaled = list(map(lambda x: (x - origin) // 4, points))
        size = pgt.Point.distance(scaled[0], scaled[-1])
        pad = size + new_dist
        print(new_dist, size, pad)
        self.draw_curve(list(reversed(list(map(lambda x: x + origin + pgt.Point(1, -1) * (new_dist / 2 - (pad + new_dist) / 2), chain(
            map(lambda x: self.rotate_around(x, (0, 0), -math.pi / 2) + (0, -pad), scaled),
            reversed(scaled),
            map(lambda x: x + (pad, 0), reversed(scaled)),
            map(lambda x: self.rotate_around(x, (0, 0), math.pi / 2) + (pad, -pad), scaled),
        ))))))

    def draw(self):
        '''Draw entire curve'''
        size = min(self.window_size) - 10
        half = size // 2
        self.draw_curve([
            self.center + (half, -half),
            self.center + (half, half),
            self.center + (-half, half),
            self.center + (-half, -half),
        ])

fractals = [SquareFractal, SierpinskiTriangle, FractalTree, HilbertCurve]
