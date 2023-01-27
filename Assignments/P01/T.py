from Shapes import Shapes
import pygame
import copy

class T(Shapes):
    def __init__(self, screen, grid):
        self.__parts = []
        self.__grid = grid
        self.__color = (240, 177, 168)
        
        #top [0]
        #has to be a deep copy or else the graphics mess up
        self.__parts.append(copy.deepcopy(self.__grid.getOrigin()))
        #left [1]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0] - self.__grid.getSlotSize(), self.__parts[0].topleft[1] + self.__grid.getSlotSize(), self.__grid.getSlotSize(), self.__grid.getSlotSize()))
        #middle [2]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0], self.__parts[0].topleft[1] + self.__grid.getSlotSize(), self.__grid.getSlotSize(), self.__grid.getSlotSize()))
        #right [3]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0] + self.__grid.getSlotSize(), self.__parts[0].topleft[1] + self.__grid.getSlotSize(), self.__grid.getSlotSize(), self.__grid.getSlotSize()))
        
        self.__direction = 'N'

        super().__init__(screen, grid, self.__parts, self.__color)

    def rotate(self, placed):
        if self.__direction == 'N':
            temp = copy.deepcopy(self.__parts[1])
            temp.x += self.__grid.getSlotSize()
            temp.y += self.__grid.getSlotSize()

            if temp.colliderect(self.__grid.getOutline()) == False:
                return
            
            for shapes in placed:
                if temp.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[1].x += self.__grid.getSlotSize()
            self.__parts[1].y += self.__grid.getSlotSize()
            self.__direction = 'E'
        elif self.__direction == 'E':
            temp = copy.deepcopy(self.__parts[0])
            temp.x -= self.__grid.getSlotSize()
            temp.y += self.__grid.getSlotSize()

            if temp.colliderect(self.__grid.getOutline()) == False:
                return
            
            for shapes in placed:
                if temp.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[0].x -= self.__grid.getSlotSize()
            self.__parts[0].y += self.__grid.getSlotSize()
            self.__direction = 'S'
        elif self.__direction == 'S':
            temp = copy.deepcopy(self.__parts[3])
            temp.x -= self.__grid.getSlotSize()
            temp.y -= self.__grid.getSlotSize()

            if temp.colliderect(self.__grid.getOutline()) == False:
                return
            
            for shapes in placed:
                if temp.collidelistall(shapes.getParts()) != []:
                    return
            
            self.__parts[3].x -= self.__grid.getSlotSize()
            self.__parts[3].y -= self.__grid.getSlotSize()
            self.__direction = 'W'
        else:
            temp0 = copy.deepcopy(self.__parts[0])
            temp0.x += self.__grid.getSlotSize()
            temp0.y -= self.__grid.getSlotSize()

            temp1 = copy.deepcopy(self.__parts[1])
            temp1.x -= self.__grid.getSlotSize()
            temp1.y -= self.__grid.getSlotSize()

            temp3 = copy.deepcopy(self.__parts[3])
            temp3.x += self.__grid.getSlotSize()
            temp3.y += self.__grid.getSlotSize()

            if not temp0.colliderect(self.__grid.getOutline()) or not temp1.colliderect(self.__grid.getOutline()) or not temp3.colliderect(self.__grid.getOutline()):
                return
            
            for shapes in placed:
                if temp0.collidelistall(shapes.getParts()) != [] or temp1.collidelistall(shapes.getParts()) != [] or temp3.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[0].x += self.__grid.getSlotSize()
            self.__parts[0].y -= self.__grid.getSlotSize()
            self.__parts[1].x -= self.__grid.getSlotSize()
            self.__parts[1].y -= self.__grid.getSlotSize()
            self.__parts[3].x += self.__grid.getSlotSize()
            self.__parts[3].y += self.__grid.getSlotSize()
            self.__direction = 'N'