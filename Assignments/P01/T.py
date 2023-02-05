from Shapes import Shapes
import pygame
import copy

class T(Shapes):
    """
    A class used to represent T shape in Tetris

    ...

    Attributes
    ----------
    grid : Grid
        The grid that the shape will be displayed on
    parts: list
        list of the parts of the shape
    color: Tuple
        Color of the shape in (R,G,B) format
    direction: char
        The direction the shape is facing

    Methods
    -------
    rotate(placed)
        rotates the shape

    """
    def __init__(self, screen, grid):
        """
        Parameters
        ----------
        screen : pygame.Display
            The screen the game is played on
        grid : Grid
            The grid that the game is played on
        """
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
        """
        Rotates the shape

        Parameters
        ----------
        placed : list
            The shapes that have already been placed
        """

        #See I shape for description of what is happening
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