from Shapes import Shapes
import pygame
import copy

class S(Shapes):
    def __init__(self, screen, grid):
        self.__parts = []
        self.__color = (242, 132, 130)
        self.__grid = grid

        #top middle [0]
        #has to be a deep copy or else the graphics mess up
        self.__parts.append(copy.deepcopy(self.__grid.getOrigin()))

        #top right [1]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0] + self.__grid.getSlotSize(), self.__parts[0].topleft[1], self.__grid.getSlotSize(), self.__grid.getSlotSize()))

        #bottom middle [2]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0], self.__parts[0].topleft[1] + self.__grid.getSlotSize(), self.__grid.getSlotSize(), self.__grid.getSlotSize()))

        #bottom left [3]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0] - self.__grid.getSlotSize(), self.__parts[0].topleft[1] + self.__grid.getSlotSize(), self.__grid.getSlotSize(), self.__grid.getSlotSize()))

        self.__direction = 'E'

        super().__init__(screen, self.__grid, self.__parts, self.__color)

    def rotate(self, placed):
        if self.__direction == 'E':
            temp2 = copy.deepcopy(self.__parts[2])
            temp2.y -= self.__grid.getSlotSize() * 2

            temp3 = copy.deepcopy(self.__parts[3])
            temp3.x += self.__grid.getSlotSize() * 2

            if not temp2.colliderect(self.__grid.getOutline()) or not temp3.colliderect(self.__grid.getOutline()):
                return
            
            for shapes in placed:
                if temp2.collidelistall(shapes.getParts()) != [] or temp3.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[2].y -= self.__grid.getSlotSize() * 2
            self.__parts[3].x += self.__grid.getSlotSize() * 2
            self.__direction = 'N'
        else:
            temp2 = copy.deepcopy(self.__parts[2])
            temp2.y += self.__grid.getSlotSize() * 2

            temp3 = copy.deepcopy(self.__parts[3])
            temp3.x -= self.__grid.getSlotSize() * 2

            if not temp2.colliderect(self.__grid.getOutline()) or not temp3.colliderect(self.__grid.getOutline()):
                return
            
            for shapes in placed:
                if temp2.collidelistall(shapes.getParts()) != [] or temp3.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[2].y += self.__grid.getSlotSize() * 2
            self.__parts[3].x -= self.__grid.getSlotSize() * 2
            self.__direction = 'E'