import pygame
from pygame.math import Vector2
from PIL import Image
from BaseSprite import BaseSprite
import Util

class Ship:
    def __init__(self, loc):
        self.__imageMul = 1.5

        self.__full = pygame.image.load(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Full health.png')
        self.__slight = pygame.image.load(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Slight damage.png')
        self.__damaged = pygame.image.load(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Damaged.png')
        self.__very = pygame.image.load(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Very damaged.png')

        self.__body = BaseSprite(self.__full, Util.scale(self.__full.get_size(), self.__imageMul), mask=True)

        engine = pygame.image.load('Ship/Main Ship/Main Ship - Engines/Main Ship - Engines - Base Engine.png')

        self.__engine = BaseSprite(engine, Util.scale(engine.get_size(), self.__imageMul), mask=True)

        self.__gunStates = []

        gunImage = Image.open('Ship/Main Ship/Main Ship - Weapons/Main Ship - Weapons - Zapper.png')

        #has 14 frames
        for i in range(14):                
            #crops to the best size for screen
            img = gunImage.crop(((gunImage.size[0] / 14) * i, 0, (gunImage.size[0] / 14) * (i + 1), gunImage.size[1]))

            img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

            self.__gunStates.append(img)

        self.__gun = BaseSprite(self.__gunStates[0], Util.scale(self.__gunStates[0].get_size(), self.__imageMul), mask=True)

        self.__ship = pygame.sprite.Group([self.__gun, self.__engine, self.__body])

        self.__ship.update('Location', loc)
        self.__position = loc

        self.__up = Vector2(0,-1)

        self.__velocity = Vector2(0)

        self.__direction = Vector2(self.__up)

        self.__acceleration = 0.25

        self.__maneuverability = 3

    def draw(self, screen):
        self.__ship.update('Move', [self.__velocity, screen])
        self.__ship.update('Rotate', self.__direction.angle_to(self.__up))
        
        self.__ship.draw(screen)

    def rotate(self, clockwise = True):
        sign = 1 if clockwise else -1
        angle = self.__maneuverability * sign
        self.__direction.rotate_ip(angle)

    def accelerate(self):
        self.__velocity += self.__direction * self.__acceleration

    def CheckCollision(self, sprite):
        didIt = [False]
        self.__ship.update('Collide', [sprite.getMask(), sprite.rect], didIt)
        return didIt[0]
