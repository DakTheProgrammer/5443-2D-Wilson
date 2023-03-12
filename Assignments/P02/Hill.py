import pygame
from PIL import Image
"""
    A class used to represent the Hill in the middle of the screen

    ...

    Attributes
    ----------
    
    image : pygame.Image
        the image for the hill
    mask : pygame.Mask
        the collider for the hill
    Rect : pygame.Rect
        the rectangle for the image

    Methods
    -------
    draw(screen)
        draws the hill on the screen
    getMask(event):
        gets the hills colliders

"""

class Hill(pygame.sprite.Sprite):
    def __init__(self, screen, y):
        """
        Parameters
        ----------
        screen : pygame.display
            the screen used by pygame
        y : int
            the bottom of the hill
        """
        self.image = self.image = Image.open('Hill/Hill.png')
        self.image = self.image.crop(self.image.getbbox())
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_size()[0] / 1.5, self.image.get_size()[1] / 1.4))
        
        self.__mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()

        #+2 just to make it blend better
        self.rect.bottomleft = (screen.get_width() * .215, y + 2)
        
    def draw(self, screen):
        """
        draws the hill

        Parameters
        ----------
        screen: pygame.display
            the screen used by pygame
        """
        #draws the mask
        #pygame.draw.lines(screen, (255,0,0), (100,100), self.__mask.outline())

        screen.blit(self.image, self.rect)

    def getMask(self):
        """
        gets the collider of the hill

        Parameters
        ----------
        """
        return self.__mask