import pygame
"""
    A class used to represent the ground rectangle

    ...

    Attributes
    ----------
    rect : pygame.Rect
        the rectangle that is the ground 

    Methods
    -------
    draw(screen)
        draws the ground
    getGroundY():
        gets the Y level of the ground

    """

class Ground:
    def __init__(self, screen):
        """
        Parameters
        ----------
        screen : pygame.display
            the screen used by pygame
        """
        self.__rect = pygame.Rect(0, screen.get_height() * .75, screen.get_width(), screen.get_height() * .25)

    def draw(self, screen):
        """
        draws the ground

        Parameters
        ----------
        screen : pygame.display
            the screen used by pygame
        """
        pygame.draw.rect(screen, (48, 200, 0), self.__rect)

    def getGroundY(self):
        """
        gets the top of the rectangle used for the ground(ground level)

        Parameters
        ----------
        """
        return self.__rect.top