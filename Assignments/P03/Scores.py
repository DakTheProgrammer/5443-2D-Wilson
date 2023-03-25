import pygame

class Scores():
    def __init__(self):
        
        self.__font = pygame.font.Font('Fonts/Lora-Bold.ttf', 20)
        self.__font.set_underline(1)
        self.__italic = pygame.font.Font('Fonts/Lora-MediumItalic.ttf', 18)

    def draw(self, screen, score, user):
        screen.blit(self.__font.render("SCORE BOARD", 1, (255,255,255)), (15, 5))
        screen.blit(self.__italic.render(str(user) +": " +str(score), 1, (255,255,255)), (15,28))
        