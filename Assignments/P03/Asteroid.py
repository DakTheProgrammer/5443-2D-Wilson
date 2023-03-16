import pygame
from BaseSprite import BaseSprite
import Util
from pygame.math import Vector2
import random

class Asteroid():
    def __init__(self, screen):
        speedMul = 2
        
        image = pygame.image.load("Environment/Asteroids/Asteroid 01 - Base.png")
        
        self.__location = Vector2(random.randrange(0, screen.get_width()),random.randrange(0, screen.get_height()))
        self.__sprite = BaseSprite(image, Util.scale(image.get_size(), 3),loc=self.__location, mask=True)
        self.__velocity = Vector2(random.uniform(-1,1) * speedMul, random.uniform(-1,1) * speedMul)
        self.__velocity = Vector2(0)
        
        
        
    def draw(self, screen):
        self.__sprite.update('Move', [self.__velocity, screen])

        self.__sprite.draw(screen)
        
    def getSprite(self):
        return self.__sprite
        
    
        