import pygame

class Score:
    def __init__(self):
        self.__font = pygame.font.Font('Assets/Font/dungeon.ttf', 32)
        self.__user = []
        self.__score = 0
        
    def update(self, score):
        self.__score = score
        
    def draw(self, screen, left, top, ):
        screen.blit(self.__font.render("SCORE " + str(self.__score), 1, (205,170,150)),(left, top))
  
        