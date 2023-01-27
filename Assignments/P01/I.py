from Shapes import Shapes
import pygame
import copy

class I(Shapes):
    def __init__(self, screen, grid):
        self.__parts = []
        self.__grid = grid
        self.__color = (246, 189, 96)

        #top [0]
        #has to be a deep copy or else the graphics mess up
        self.__parts.append(copy.deepcopy(self.__grid.getOrigin()))
        #top center [1]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0], self.__parts[0].topleft[1] + self.__grid.getSlotSize(), self.__grid.getSlotSize(), self.__grid.getSlotSize()))
        #bottom center [2]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0], self.__parts[0].topleft[1] + self.__grid.getSlotSize() * 2, self.__grid.getSlotSize(), self.__grid.getSlotSize()))
        #bottom [3]
        self.__parts.append(pygame.Rect(self.__parts[0].topleft[0], self.__parts[0].topleft[1] + self.__grid.getSlotSize() * 3, self.__grid.getSlotSize(), self.__grid.getSlotSize()))
        
        self.__direction = 'N'

        super().__init__(screen, grid, self.__parts, self.__color)

    def rotate(self, placed):
        if self.__direction == 'N':
            temp1 = copy.deepcopy(self.__parts[1])
            temp1.x += self.__grid.getSlotSize()
            temp1.y -= self.__grid.getSlotSize()

            temp2 = copy.deepcopy(self.__parts[2])
            temp2.x += self.__grid.getSlotSize() * 2
            temp2.y -= self.__grid.getSlotSize() * 2

            temp3 = copy.deepcopy(self.__parts[3])
            temp3.x += self.__grid.getSlotSize() * 3 
            temp3.y -= self.__grid.getSlotSize() * 3

            if not temp1.colliderect(self.__grid.getOutline()) or not temp2.colliderect(self.__grid.getOutline()) or not temp3.colliderect(self.__grid.getOutline()):
                return
            
            for shapes in placed:
                if temp1.collidelistall(shapes.getParts()) != [] or temp2.collidelistall(shapes.getParts()) != [] or temp3.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[1].x += self.__grid.getSlotSize()
            self.__parts[1].y -= self.__grid.getSlotSize()
            self.__parts[2].x += self.__grid.getSlotSize() * 2
            self.__parts[2].y -= self.__grid.getSlotSize() * 2
            self.__parts[3].x += self.__grid.getSlotSize() * 3
            self.__parts[3].y -= self.__grid.getSlotSize() * 3
            self.__direction = 'E'
        else:
            temp1 = copy.deepcopy(self.__parts[1])
            temp1.x -= self.__grid.getSlotSize()
            temp1.y += self.__grid.getSlotSize()

            temp2 = copy.deepcopy(self.__parts[2])
            temp2.x -= self.__grid.getSlotSize() * 2
            temp2.y += self.__grid.getSlotSize() * 2

            temp3 = copy.deepcopy(self.__parts[3])
            temp3.x -= self.__grid.getSlotSize() * 3 
            temp3.y += self.__grid.getSlotSize() * 3

            if not temp1.colliderect(self.__grid.getOutline()) or not temp2.colliderect(self.__grid.getOutline()) or not temp3.colliderect(self.__grid.getOutline()):
                return
            
            for shapes in placed:
                if temp1.collidelistall(shapes.getParts()) != [] or temp2.collidelistall(shapes.getParts()) != [] or temp3.collidelistall(shapes.getParts()) != []:
                    return

            self.__parts[1].x -= self.__grid.getSlotSize()
            self.__parts[1].y += self.__grid.getSlotSize()
            self.__parts[2].x -= self.__grid.getSlotSize() * 2
            self.__parts[2].y += self.__grid.getSlotSize() * 2
            self.__parts[3].x -= self.__grid.getSlotSize() * 3
            self.__parts[3].y += self.__grid.getSlotSize() * 3
            self.__direction = 'N'