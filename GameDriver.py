from cmath import rect
from turtle import Screen, width
import pygame
from SpriteSheet import SpriteSheet
from Map import Map
from Player import Player

class GameDriver:
    def __init__(self, title, background = (255,255,255), height = 800, width = 800, fps = 60):
        pygame.init()

        self.__background = background
        self.__screen = pygame.display.set_mode((width,height))
        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0
        self.__running = True

        pygame.display.set_caption(title)
        
        startLevel = './Levels/Start.tmx'

        self.__spriteSheet = SpriteSheet(startLevel)
        self.__map = Map(startLevel, self.__spriteSheet.getSpritesList())

        #41 is p1 default character
        self.__playerOne = Player(41, self.__spriteSheet.getSpritesList())

    def GameLoop(self):
        while self.__running:
            self.__draw()

            self.__handleEvents()

            self.__delta = self.__clock.tick(self.__fps)

    def __draw(self):
        
        self.__screen.fill(self.__background)
        self.__map.draw(self.__screen)
        self.__playerOne.draw(self.__screen)
        
        zoom = pygame.transform.rotozoom(self.__screen.copy(), 0, 2)
        zoomRec = zoom.get_rect()

        #zoomRec.center = (self.__playerOne.rect.centerx + (1.5 * self.__screen.get_width()), self.__playerOne.rect.centery + (1.5 * self.__screen.get_height()))
        #print(self.__playerOne.rect.center, zoomRec.center)
        
        self.__screen.blit(zoom, zoomRec)
        
        pygame.display.flip()

    def __handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False~