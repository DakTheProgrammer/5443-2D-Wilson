from Shapes import Shapes
import pygame
import copy

class L(Shapes):
    def __init__(self, screen, grid):
        self.__parts = []
        self.__color = (132, 165, 157)
        self.__grid = grid

        #top [0]
        #has to be a deep copy or else the graphics mess up
        self.__parts.append(copy.deepcopy(self.__grid.getOrigin()))
        
        #middle [1]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0], self.__parts[0].topleft[1] + self.__grid.getSlotSize(), self.__grid.getSlotSize(), self.__grid.getSlotSize()))

        #bottom left [2]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0], self.__parts[0].topleft[1] + self.__grid.getSlotSize() * 2, self.__grid.getSlotSize(), self.__grid.getSlotSize()))

        #bottom right [3]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0] + self.__grid.getSlotSize(), self.__parts[0].topleft[1] + self.__grid.getSlotSize() * 2, self.__grid.getSlotSize(), self.__grid.getSlotSize()))

        self.__direction = 'N'

        super().__init__(screen, self.__grid, self.__parts, self.__color)

    def rotate(self, placed):
        if self.__direction == 'N':
            temp0 = copy.deepcopy(self.__parts[0])
            temp0.x += self.__grid.getSlotSize() * 2
            temp0.y += self.__grid.getSlotSize() * 2

            temp1 = copy.deepcopy(self.__parts[1])
            temp1.y += self.__grid.getSlotSize() * 2

            if not temp0.colliderect(self.__grid.getOutline()) or not temp1.colliderect(self.__grid.getOutline()):
                return
            
            for shapes in placed:
                if temp0.collidelistall(shapes.getParts()) != [] or temp1.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[0].x += self.__grid.getSlotSize() * 2
            self.__parts[0].y += self.__grid.getSlotSize() * 2
            self.__parts[1].y += self.__grid.getSlotSize() * 2

            self.__direction = 'E'
        elif self.__direction == 'E':
            temp0 = copy.deepcopy(self.__parts[0])
            temp0.x -= self.__grid.getSlotSize()
            temp0.y += self.__grid.getSlotSize()

            temp1 = copy.deepcopy(self.__parts[1])
            temp1.x += self.__grid.getSlotSize()
            temp1.y += self.__grid.getSlotSize()

            if not temp0.colliderect(self.__grid.getOutline()) or not temp1.colliderect(self.__grid.getOutline()):
                return
            
            for shapes in placed:
                if temp0.collidelistall(shapes.getParts()) != [] or temp1.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[0].x -= self.__grid.getSlotSize()
            self.__parts[0].y += self.__grid.getSlotSize()
            self.__parts[1].x += self.__grid.getSlotSize()
            self.__parts[1].y += self.__grid.getSlotSize()

            self.__direction = 'S'
        elif self.__direction == 'S':
            temp0 = copy.deepcopy(self.__parts[0])
            temp0.x -= self.__grid.getSlotSize() * 2
            temp0.y -= self.__grid.getSlotSize()

            temp1 = copy.deepcopy(self.__parts[1])
            temp1.y -= self.__grid.getSlotSize() * 3

            if not temp0.colliderect(self.__grid.getOutline()) or not temp1.colliderect(self.__grid.getOutline()):
                return
            
            for shapes in placed:
                if temp0.collidelistall(shapes.getParts()) != [] or temp1.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[0].x -= self.__grid.getSlotSize() * 2
            self.__parts[0].y -= self.__grid.getSlotSize()
            self.__parts[1].y -= self.__grid.getSlotSize() * 3

            self.__direction = 'W'
        else:
            temp0 = copy.deepcopy(self.__parts[0])
            temp0.x += self.__grid.getSlotSize()
            temp0.y -= self.__grid.getSlotSize() * 2

            temp1 = copy.deepcopy(self.__parts[1])
            temp1.x -= self.__grid.getSlotSize()

            if not temp0.colliderect(self.__grid.getOutline()) or not temp1.colliderect(self.__grid.getOutline()):
                return
            
            for shapes in placed:
                if temp0.collidelistall(shapes.getParts()) != [] or temp1.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[0].x += self.__grid.getSlotSize()
            self.__parts[0].y -= self.__grid.getSlotSize() * 2
            self.__parts[1].x -= self.__grid.getSlotSize()

            self.__direction = 'N'