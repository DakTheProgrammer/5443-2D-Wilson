import pygame
import copy
import random

class Shapes:
    def __init__(self, screen, grid, parts, color):
        self.__parts = parts
        self.__screen = screen
        self.__grid = grid
        self.__color = color
    
    def draw(self):
        for recs in self.__parts:
            pygame.draw.rect(self.__screen, self.__color, recs)

    def rotate(self, placed):
        pass

    def move(self):
        for recs in self.__parts:
            recs.y += self.__grid.getSlotSize()
    
    def right(self, OtherShapes):
        for recs in self.__parts:
            temp = copy.deepcopy(recs)
            temp.x += self.__grid.getSlotSize()
            if temp.colliderect(self.__grid.getOutline()) == False:
                return
            for shapes in OtherShapes:
                if temp.collidelistall(shapes.getParts()) != []:
                    return

        for recs in self.__parts:
            recs.x += self.__grid.getSlotSize()
    
    def left(self, OtherShapes):
        for recs in self.__parts:
            temp = copy.deepcopy(recs)
            temp.x -= self.__grid.getSlotSize()
            if temp.colliderect(self.__grid.getOutline()) == False:
                return
            for shapes in OtherShapes:
                if temp.collidelistall(shapes.getParts()) != []:
                    return

        for recs in self.__parts:
            recs.x -= self.__grid.getSlotSize()

    def isGrounded(self, OtherShapes = None):
        for recs in self.__parts:
            temp = copy.deepcopy(recs)
            temp.y += self.__grid.getSlotSize()
            if not temp.colliderect(self.__grid.getOutline()):
                return True
            
            if OtherShapes != None:
                for shapes in OtherShapes:
                    if temp.collidelistall(shapes.getParts()) != []:
                        return True
                    
    def gameOver(self, placed):
        for piece in placed:
            for part in piece.getParts():
                if part.collidelistall(self.__parts) != []:
                    return True
                
        return False


    def getParts(self):
        return self.__parts
    
    def getColor(self):
        return self.__color
    
    def badPiece(self):
        self.__color = (255, 0,0)