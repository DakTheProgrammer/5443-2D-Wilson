import pygame

class HealthBar():
    def __init__(self,screen):
        self.__healthBar = pygame.Rect(screen.get_width()-120, 30, 100, 15)
        self.__healthBarColor = (0,255,0)
        self.__healthBarBGColor = (255,0,0)
        self.__healthBarBG = pygame.Rect(screen.get_width()-120, 30,100,15)
        self.__font = pygame.font.Font('Fonts/Lora-Bold.ttf', 20)
        self.__healthText = self.__font.render("HEALTH", 1, (255,255,255))
    def draw(self, screen):
        screen.blit(self.__healthText,(screen.get_width()-111, 5))
        pygame.draw.rect(screen, self.__healthBarBGColor, self.__healthBarBG)
        pygame.draw.rect(screen, self.__healthBarColor, self.__healthBar)
        
    def update(self, health):
        self.__healthBar.width = health