import pygame
from cmath import sqrt
from PIL import Image

class Weapon(pygame.sprite.Sprite):
    def __init__(self, default, sheet):
        
        self.offset = int(sqrt(len(sheet) - 1).real)
        self.__sprites = sheet
        handle = sheet[default]
        blade = sheet[default - self.offset]