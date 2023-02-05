from I import I
from O import O
from T import T
from L import L
from S import S
import pygame
import copy

class NextBox:
    """
    A class used to represent the next shape box in Tetris

    ...

    Attributes
    ----------
    screen : pygame.Display
        a screen object used to determine screen metrics
    color : tuple
        the (R,G,B) values of the color of the box
    box: pygame.Rect
        rectangle that stores the shape
    font: pygame.Font
        font for the text above the box 
    fontRender: pygame.Font.Render
        The renderer for the font
    shapeColor: tuple
        the (R,G,B) values of the color of the shape

    Methods
    -------
    draw()
        draws the Next box
    setPiece(piece)
        sets the piece inside the box
    """
    def __init__(self, screen, shape):
        """
        Parameters
        ----------
        screen : pygame.Display
            The screen the game is played on
        shape : Shape
            The shape that goes in the box
        """
        self.__screen = screen
        self.__color = (208, 220, 216)
        self.__box = pygame.Rect(screen.get_width() * .65, screen.get_width() * .1, self.__screen.get_width() / 4.5, self.__screen.get_width() / 4.5)
        self.__font = pygame.font.Font("Fonts/Lora-Bold.ttf", 35)
        self.__fontRender = self.__font.render("Next Piece", True, (self.__color))
        
        self.setPiece(shape)
        
    def draw(self):
        """
        Parameters
        ----------
        None
        """
        pygame.draw.rect(self.__screen, self.__color, self.__box, 2)

        for shapes in self.__shape:
            pygame.draw.rect(self.__screen, self.__shapeColor, shapes)
            pygame.draw.rect(self.__screen, (57, 62, 70), shapes, 2)

        self.__screen.blit(self.__fontRender, (self.__box.topleft[0], self.__box.topleft[1] - self.__font.get_linesize()))

    def setPiece(self, piece):
        """
        Parameters
        ----------
        piece : Shape
            Sets the pice in the box
        """
        self.__shape = copy.deepcopy(piece.getParts())
        self.__shapeColor = piece.getColor()

        #moves the shape around based on its type to ensure a good look
        for shapes in self.__shape:
            if(type(piece) == T):   
                shapes.x += self.__box.x - shapes.width - .5 * self.__box.width
                shapes.y += self.__box.top + self.__box.height / 3.5
            elif(type(piece) == I):
                shapes.x += self.__box.x - shapes.width - .5 * self.__box.width
                #20% buffer
                shapes.y += self.__box.top + self.__box.height / 20
            elif(type(piece) == O):
                shapes.x += self.__box.x - shapes.width - .625 * self.__box.width
                shapes.y += self.__box.top + self.__box.height / 3.5
            elif(type(piece) == S):
                shapes.x += self.__box.x - shapes.width - .5 * self.__box.width
                shapes.y += self.__box.top + self.__box.height / 3.5
            else:
                shapes.x += self.__box.x - shapes.width - .625 * self.__box.width
                shapes.y += self.__box.top + self.__box.height / 7
