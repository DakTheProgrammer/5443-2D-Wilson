from Shapes import Shapes
import pygame
import copy

class O(Shapes):
    def __init__(self, screen, grid):
        self.__parts = []
        self.__color = (224, 185, 143)

        #top left [0]
        #has to be a deep copy or else the graphics mess up
        self.__parts.append(copy.deepcopy(grid.getOrigin()))
        #top right [1]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0] + grid.getSlotSize(), self.__parts[0].topleft[1], grid.getSlotSize(), grid.getSlotSize()))
        #bottom left [2]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0], self.__parts[0].topleft[1] + grid.getSlotSize(), grid.getSlotSize(), grid.getSlotSize()))
        #bottom right [3]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0] + grid.getSlotSize(), self.__parts[0].topleft[1] + grid.getSlotSize(), grid.getSlotSize(), grid.getSlotSize()))

        super().__init__(screen, grid, self.__parts, self.__color)