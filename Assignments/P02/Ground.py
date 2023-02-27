import pygame

class Ground:
    def __init__(self, screen):
        self.__rect = pygame.Rect(0, screen.get_height() * .75, screen.get_width(), screen.get_height() * .25)

    def draw(self, screen):
        pygame.draw.rect(screen, (48, 200, 0), self.__rect)

    def getGroundY(self):
        return self.__rect.top