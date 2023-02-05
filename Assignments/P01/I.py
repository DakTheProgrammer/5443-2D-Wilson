from Shapes import Shapes
import pygame
import copy

class I(Shapes):
    """
    A class used to represent I shape in Tetris

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
        """
        Rotates the shape

        Parameters
        ----------
        placed : list
            The shapes that have already been placed
        """
        if self.__direction == 'N':
            #used to store a copy to see if shape can move (for collision detection)
            temp1 = copy.deepcopy(self.__parts[1])
            temp1.x += self.__grid.getSlotSize()
            temp1.y -= self.__grid.getSlotSize()

            temp2 = copy.deepcopy(self.__parts[2])
            temp2.x += self.__grid.getSlotSize() * 2
            temp2.y -= self.__grid.getSlotSize() * 2

            temp3 = copy.deepcopy(self.__parts[3])
            temp3.x += self.__grid.getSlotSize() * 3 
            temp3.y -= self.__grid.getSlotSize() * 3

            #checks if it can rotate due to the grid outlines via collision of temp
            if not temp1.colliderect(self.__grid.getOutline()) or not temp2.colliderect(self.__grid.getOutline()) or not temp3.colliderect(self.__grid.getOutline()):
                return
            
            #checks if it can rotate due to placed shapes
            for shapes in placed:
                if temp1.collidelistall(shapes.getParts()) != [] or temp2.collidelistall(shapes.getParts()) != [] or temp3.collidelistall(shapes.getParts()) != []:
                    return

            #moves the parts accordingly
            self.__parts[1].x += self.__grid.getSlotSize()
            self.__parts[1].y -= self.__grid.getSlotSize()
            self.__parts[2].x += self.__grid.getSlotSize() * 2
            self.__parts[2].y -= self.__grid.getSlotSize() * 2
            self.__parts[3].x += self.__grid.getSlotSize() * 3
            self.__parts[3].y -= self.__grid.getSlotSize() * 3
            self.__direction = 'E'
        else:
            #see above documentation
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