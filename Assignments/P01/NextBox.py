from I import I
from O import O
from T import T
from L import L
from S import S
import pygame
import copy

class NextBox:
    def __init__(self, screen, shape):
        self.__screen = screen
        self.__color = (208, 220, 216)
        self.__box = pygame.Rect(screen.get_width() * .65, screen.get_width() * .1, self.__screen.get_width() / 4.5, self.__screen.get_width() / 4.5)
        self.__font = pygame.font.Font("Fonts/Lora-Bold.ttf", 35)
        self.__fontRender = self.__font.render("Next Piece", True, (self.__color))
        
        self.setPiece(shape)
        
    def draw(self):
        pygame.draw.rect(self.__screen, self.__color, self.__box, 2)

        for shapes in self.__shape:
            pygame.draw.rect(self.__screen, self.__shapeColor, shapes)
            pygame.draw.rect(self.__screen, (57, 62, 70), shapes, 2)

        self.__screen.blit(self.__fontRender, (self.__box.topleft[0], self.__box.topleft[1] - self.__font.get_linesize()))

    def setPiece(self, piece):
        self.__shape = copy.deepcopy(piece.getParts())
        self.__shapeColor = piece.getColor()

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
