from Shapes import Shapes
import pygame
import copy

class S(Shapes):
    def __init__(self, screen, grid):
        self.__parts = []
        self.__color = (242, 132, 130)
        super().__init__(screen, grid, self.__parts, self.__color)