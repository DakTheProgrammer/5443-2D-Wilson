import pygame
class Scores():
    def __init__(self):
        self.__font = pygame.font.Font('Fonts/Lora-Bold.ttf', 20)
        self.__italic = pygame.font.Font('Fonts/Lora-MediumItalic.ttf', 17)
        
    def draw(self, screen, score):
        screen.blit(self.__font.render("TOP SCORE", 1, (255,255,255)), (15, 5))
        screen.blit(self.__italic.render("Player 1: " + str(score), 1, (255,255,255)), (20,25))
        