import pygame
from PIL import Image

class Crater:
    def __init__(self, loc):
        self.image = Image.open('Crater/Crater.png')
        self.image = self.image.crop(self.image.getbbox())
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_size()[0] / 2, self.image.get_size()[1] / 2))

        self.__mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()

        self.rect.center = loc
        
    def draw(self, screen):
        #draws the mask
        #pygame.draw.lines(screen, (255,0,0), (100,100), self.__mask.outline())

        screen.blit(self.image, self.rect)

    def getMask(self):
        return self.__mask