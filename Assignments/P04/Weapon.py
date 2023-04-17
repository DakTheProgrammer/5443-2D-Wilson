import pygame
from cmath import sqrt
from Tile import Tile
from copy import deepcopy

class Weapon(pygame.sprite.Sprite):
    def __init__(self, default, sheet, rec):
        
        self.offset = int(sqrt(len(sheet) - 1).real)
        self.__sprites = sheet
        handleRec = deepcopy(rec)
        handleRec.top -= rec.width / 2
        handle = Tile(sheet[default], handleRec, default)
        bladeRec = deepcopy(rec)
        bladeRec.top -= rec.width / 2 * 3
        blade = Tile(sheet[default - self.offset], bladeRec, default - self.offset)
        self.__group = pygame.sprite.Group([handle, blade])
        
        
    def draw(self, screen):
        self.__group.draw(screen)