import pygame
from Background import Background
from Ship import Ship

class GameDriver:
    def __init__(self, title, backgroundColor = (255,255,255), height = 800, width = 800, fps = 60):
        ########################################################
        pygame.init()

        self.__backgroundColor = backgroundColor
        
        self.__screen = pygame.display.set_mode((height,width))
        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0
        self.__running = True

        pygame.display.set_caption(title)

        #########################################################

        self.__background = Background(
            [
            'Environment\Backgrounds\Condensed\Starry background  - Layer 01 - Void.png',
            'Environment\Backgrounds\Condensed\Starry background  - Layer 02 - Stars.png',
            'Environment\Backgrounds\Condensed\Starry background  - Layer 03 - Stars.png'
            ], 9,self.__screen, 4
        )

        self.__ship = Ship()


    def GameLoop(self):
        while self.__running:
            self.__Draw()

            self.__HandleEvents()

            self.__delta = self.__clock.tick(self.__fps)

    def __Draw(self):
        self.__screen.fill(self.__backgroundColor)
        self.__background.draw(self.__screen)

        self.__ship.draw(self.__screen)

        pygame.display.flip()

    def __HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False