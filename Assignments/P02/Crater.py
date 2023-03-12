import pygame
from PIL import Image

"""
    A class used to represent the Crater sprite

    ...

    Attributes
    ----------
    
    image : pygame.Image
        the image used for the sprite
    mask : Pygame.Mask
        the collider of the sprite
    rect : pygame.Rect
        the rectangle of the image

    Methods
    -------
    draw(screen)
        draws the sprite
    getMask():
        gets the collider of the object
    """
class Crater:
    def __init__(self, loc):
        """
        Parameters
        ----------
        loc : tuple
            location of the crater
        """
        self.image = Image.open('Crater/Crater.png')
        self.image = self.image.crop(self.image.getbbox())
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_size()[0] / 2, self.image.get_size()[1] / 2))

        self.__mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()

        self.rect.center = loc
        
    def draw(self, screen):
        """
        draws a crater 

        Parameters
        ----------
        screen : pygame.display
            the screen of the game to draw on
        """
        #draws the mask
        #pygame.draw.lines(screen, (255,0,0), (100,100), self.__mask.outline())

        screen.blit(self.image, self.rect)

    def getMask(self):
        """
        gets the collider of the crater

        Parameters
        ----------
        """
        return self.__mask