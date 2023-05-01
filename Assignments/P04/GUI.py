import pygame
from HealthBar import HealthBar

class GUI:
    def __init__(self, sheet):
        self.__healthBar = HealthBar(sheet)
        
    def draw(self, screen, left, top):
        self.__healthBar.draw(screen, left, top)