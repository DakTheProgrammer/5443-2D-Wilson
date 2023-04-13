import pygame
from Map import Map

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
        
        self.map = Map('./Levels/Test.tmx')

    def GameLoop(self):
        while self.__running:
            self.__draw()

            self.__handleEvents()

            self.__delta = self.__clock.tick(self.__fps)

    def __draw(self):
        self.__screen.fill((255,255,255))
        
        self.map.draw(self.__screen)
        
        pygame.display.flip()

    def __handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False