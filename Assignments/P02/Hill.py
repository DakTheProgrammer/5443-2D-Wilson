import pygame
from PIL import Image

class Hill(pygame.sprite.Sprite):
    def __init__(self, screen, y):
        self.image = self.image = Image.open('Hill/Hill.png')
        self.image = self.image.crop(self.image.getbbox())
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_size()[0] / 1.5, self.image.get_size()[1] / 1.4))
        
        self.__mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()

        #+2 just to make it blend better
        self.rect.bottomleft = (screen.get_width() * .215, y + 2)
        
    def draw(self, screen):
        #draws the mask
        #pygame.draw.lines(screen, (255,0,0), (100,100), self.__mask.outline())

        screen.blit(self.image, self.rect)

    def getMask(self):
        return self.__mask