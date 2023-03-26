import pygame
from BaseSprite import BaseSprite
import Util
from pygame.math import Vector2
import random

class Asteroid():
    def __init__(self, screen, scale, loc = None, vel = None):
        self.__scale = scale
        speedMul = 2
        
        image = pygame.image.load("Environment/Asteroids/Asteroid 01 - Base.png")
        
        if loc == None:
            self.__location = Vector2(random.randrange(image.get_size()[0], screen.get_width()) / 3,random.randrange(image.get_size()[1], screen.get_height() - 50) / 3)
        else:
            self.__location = loc
        
        self.__sprite = BaseSprite(image, Util.scale(image.get_size(), self.__scale),loc=self.__location, mask=True)
        if vel == None:
            self.__velocity = Vector2(random.uniform(-1,1) * speedMul + 1, random.uniform(-1,1) * speedMul + 1)
        else:
            self.__velocity = Vector2(vel)
        
        
        
    def draw(self, screen):
        self.__sprite.update('Move', [self.__velocity, screen])

        self.__sprite.draw(screen)
        
    def getSprite(self):
        return self.__sprite
        
    def getLocation(self):
        return self.__sprite.rect.topleft
    
    def getScale(self):
        return self.__scale
    
    def getVelocity(self):
        return self.__velocity.x, self.__velocity.y
    
    def getSize(self):
        return self.__scale