import pygame

class Scores():
    def __init__(self):
        self.__font = pygame.font.Font('Fonts/Lora-Bold.ttf', 20)
        self.__italic = pygame.font.Font('Fonts/Lora-MediumItalic.ttf', 18)

    def draw(self, screen, score):
        screen.blit(self.__font.render("SCORE BOARD", 1, (255,255,255)), (15, 5))
        screen.blit(self.__italic.render("Player: " +str(score), 1, (255,255,255)), (30,25))
        