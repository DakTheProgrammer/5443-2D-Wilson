import pygame

class Scores():
    def __init__(self, player, color):
        
        self.__font = pygame.font.Font('Fonts/Lora-Bold.ttf', 20)
        self.__font.set_underline(1)
        self.__italic = pygame.font.Font('Fonts/Lora-MediumItalic.ttf', 18)
        self.__user = []
        self.addPlayer(player, color)
        
    def addPlayer(self, Id, color):
        self.__user.append([Id,0, color])
        
        
    def update(self, Id, Score):
        for tup in self.__user:
            if tup[0] == Id:
                tup[1] = Score
                self.__user.sort(key=lambda tup: tup[1], reverse=True)
                break
        
    def draw(self, screen):
        screen.blit(self.__font.render("SCORE BOARD", 1, (255,255,255)), (15, 5))
        pos = 28
        for player in self.__user:
            screen.blit(self.__italic.render(str(player[0]) +": "+ str(player[1]), 1, player[2]), (15,pos))
            pos += 22
        