from Shapes import Shapes
import pygame
import copy

class L(Shapes):
    def __init__(self, screen, grid):
        self.__parts = []
        self.__color = (132, 165, 157)
        super().__init__(screen, grid, self.__parts, self.__color)