import pygame
from PIL import Image
from BaseSprite import BaseSprite


class Ship:
    def __init__(self):
        self.__full = pygame.image.load(
            'Ship\Main Ship\Main Ship - Bases\Main Ship - Base - Full health.png')
        self.__slight = pygame.image.load(
            'Ship\Main Ship\Main Ship - Bases\Main Ship - Base - Slight damage.png')
        self.__damaged = pygame.image.load(
            'Ship\Main Ship\Main Ship - Bases\Main Ship - Base - Damaged.png')
        self.__very = pygame.image.load(
            'Ship\Main Ship\Main Ship - Bases\Main Ship - Base - Very damaged.png')

        self.__body = BaseSprite(self.__full, self.__full.get_size())

        engine = pygame.image.load('Ship\Main Ship\Main Ship - Engines\Main Ship - Engines - Base Engine.png')

        self.__engine = BaseSprite(engine, engine.get_size())

        self.__gunStates = []

        gunImage = Image.open('Ship\Main Ship\Main Ship - Weapons\Main Ship - Weapons - Zapper.png')

        #has 14 frames
        for i in range(14):                
            #crops to the best size for screen
            img = gunImage.crop(((gunImage.size[0] / 14) * i, 0, (gunImage.size[0] / 14) * (i + 1), gunImage.size[1]))

            img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

            self.__gunStates.append(img)

        self.__gun = BaseSprite(self.__gunStates[0], self.__gunStates[0].get_size())

        self.__ship= pygame.sprite.Group([self.__gun, self.__engine, self.__body])

    def draw(self, screen):
        self.__ship.draw(screen)
        self.__ship.update()
