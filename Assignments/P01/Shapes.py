import pygame
import copy
import random

class Shapes:
    """
    A class used to represent the overlay grid that actually holds
    the tetris game

    ...

    Attributes
    ----------
    screen : pygame.Display
        a screen object used to determine screen metrics
    parts : list
        a list of the parts of the shape
    grid : Grid
        The grid that the shape will be displayed on
    color : tuple
        the (R,G,B) values of the color of the shape

    Methods
    -------
    draw()
        draws the shape
    rotate(placed)
        rotates the shape
    move()
        moves the shape down 1 grid unit
    right(OtherShapes)
        moves the shape to the right if possible
    left(OtherShapes)
        moves the shape to the left if possible
    isGrounded(OtherShapes = None)
        checks if the shape is grounded when none 
        is passed used to loop for movement
    gameOver(placed)
        checks for a game over scenario
    getParts()
        returns the parts of the shape
    getColor()
        returns the color of the shape
    badPiece()
        makes the color of the piece red
    """
    def __init__(self, screen, grid, parts, color):
        """
        Parameters
        ----------
        screen : pygame.Display
            The screen the game is played on
        grid : Grid
            The grid that the game is played on
        parts : list
            The parts of the shape
        color : tuple
            The color of the shape in (R,G,B) format
        """
        self.__parts = parts
        self.__screen = screen
        self.__grid = grid
        self.__color = color
    
    def draw(self):
        """
        draws the shape 

        Parameters
        ----------
        None
        """
        for recs in self.__parts:
            pygame.draw.rect(self.__screen, self.__color, recs)

    def rotate(self, placed):
        """
        rotates the shape

        Parameters
        ----------
        placed : list
            the shapes that have already been placed
        """
        pass

    def move(self):
        """
        moves the shape one unit down

        Parameters
        ----------
        None
        """
        for recs in self.__parts:
            recs.y += self.__grid.getSlotSize()
    
    def right(self, OtherShapes):
        """
        moves the shape one unit to the right if possible

        Parameters
        ----------
        OtherShapes : list
            the shapes that have already been placed
        """
        for recs in self.__parts:
            temp = copy.deepcopy(recs)
            temp.x += self.__grid.getSlotSize()
            #return if shape hits outline
            if temp.colliderect(self.__grid.getOutline()) == False:
                return
            for shapes in OtherShapes:
                #returns if the shape hits any other piece
                if temp.collidelistall(shapes.getParts()) != []:
                    return

        #move each part to the right
        for recs in self.__parts:
            recs.x += self.__grid.getSlotSize()
    
    def left(self, OtherShapes):
        """
        moves the shape one unit to the left if possible

        Parameters
        ----------
        OtherShapes : list
            the shapes that have already been placed
        """
        for recs in self.__parts:
            temp = copy.deepcopy(recs)
            temp.x -= self.__grid.getSlotSize()
            #return if shape hits outline
            if temp.colliderect(self.__grid.getOutline()) == False:
                return
            for shapes in OtherShapes:
                #returns if the shape hits any other piece
                if temp.collidelistall(shapes.getParts()) != []:
                    return

        #move each part to the right
        for recs in self.__parts:
            recs.x -= self.__grid.getSlotSize()

    def isGrounded(self, OtherShapes = None):
        """
        Checks if the shape is grounded. If nothing is passed
        in can be used to loop through moving shape all the way
        down.

        Parameters
        ----------
        OtherShapes : list, optional
            the shapes that have already been placed
        """
        for recs in self.__parts:
            temp = copy.deepcopy(recs)
            temp.y += self.__grid.getSlotSize()
            #if collides with the outline it is grounded
            if not temp.colliderect(self.__grid.getOutline()):
                return True
            
            #if it hits any other shape it is grounded
            if OtherShapes != None:
                for shapes in OtherShapes:
                    if temp.collidelistall(shapes.getParts()) != []:
                        return True
                    
    def gameOver(self, placed):
        """
        checks for game over scenario

        Parameters
        ----------
        placed : list
            the shapes that have already been placed

        Returns
        -------
        bool
            the result of if there is a game over
        """
        #when a piece is first spawned if it collides with any shape its game over
        for piece in placed:
            for part in piece.getParts():
                if part.collidelistall(self.__parts) != []:
                    return True
                
        return False

    def getParts(self):
        """
        returns the parts of the shape

        Parameters
        ----------
        None

        Returns
        -------
        list
            the parts of the shape
        """
        return self.__parts
    
    def getColor(self):
        """
        returns the color of the shape

        Parameters
        ----------
        None

        Returns
        -------
        tuple
            the color of the shape
        """
        return self.__color
    
    def badPiece(self):
        """
        makes the piece the color red

        Parameters
        ----------
        None
        """
        self.__color = (255, 0,0)