import pygame
from HealthBar import HealthBar
from Score import Score
class GUI:
    def __init__(self, sheet):
        self.__healthBar = HealthBar(sheet)
        self.__score = Score()
        
    def update(self, health, score):
        self.__score.update(score)
        self.__healthBar.update(health)
        
    def draw(self, screen, left, top):
        self.__score.draw(screen, (left+16), (top + 16))
        self.__healthBar.draw(screen, (left+16), (top+48))
        
   