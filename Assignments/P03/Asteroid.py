import pygame
from BaseSprite import BaseSprite
import Util
from pygame.math import Vector2
import random

class Asteroid():
    """
    An Asteroid class to represent the asteroids in the game
    
    Attributes
    ----------
    __scale : float
        the scale of the asteroid
    speedMul : int
        the speed multiplier of the asteroid
    __location : Vector2
        the location of the asteroid 
    __sprite : BaseSprite
        the sprite of the asteroid
    __velocity : Vector2
        the velocity of the asteroid
    
    Methods
    -------
    draw(screen, delta) :
        draws the asteroid
    getSprite() :
        gets the sprite of the asteroid
    getLocation() :
        gets the location of the asteroid
    getScale() :
        gets the scale of the asteroid
    getVelocity() :
        gets the velocity of the asteroid
    getSize() :
        gets the size of the asteroid
    
    """
    def __init__(self, screen, scale, loc = None, vel = None):
        """
        Parameters
        ----------
            screen : pygame.display
            scale : float
            loc : optional
                Defaults to None
            vel : optional
                Defaults to None
        """
        self.__scale = scale
        speedMul = 2
        
        image = pygame.image.load("Environment/Asteroids/Asteroid 01 - Base.png")
        
        if loc == None:
            self.__location = Vector2(random.randrange(0, 700),random.randrange(0, 500))
            
        else:
            self.__location = loc
        
        self.__sprite = BaseSprite(image, Util.scale(image.get_size(), self.__scale),loc=self.__location, mask=True)
        if vel == None:
            self.__velocity = Vector2(random.uniform(-1,1) * speedMul + 1, random.uniform(-1,1) * speedMul + 1)
        else:
            self.__velocity = Vector2(vel)
        
        
        
    def draw(self, screen, delta):
        """
        Draws the asteroids on the scteen

        Parameters
        -----------
            screen : pygame.display
            delta : 
        """
        self.__sprite.update('Move', [self.__velocity, screen, delta])

        self.__sprite.draw(screen)
        
    def getSprite(self):
        """
        Gets the sprite for the asteroid
        
        Returns
        -------
            asteroid sprite
        """
        return self.__sprite
        
    def getLocation(self):
        """
        Gets the location of the asteroid
        
        Returns
        -------
            sprite location
        """
        return self.__sprite.rect.topleft
    
    def getScale(self):
        """
        Gets the scale of the asteroid
        
        Returns
        -------
            scale of the asteroid
        """
        return self.__scale
    
    def getVelocity(self):
        """
        Gets the velocity of the asteroid
        
        Returns
        -------
            asteroids velocity
        """
        return self.__velocity.x, self.__velocity.y
    
    def getSize(self):
        """
        Gets the size of the asteroid
        
        Returns
        -------
            size of the asteroid
        """
        return self.__scale