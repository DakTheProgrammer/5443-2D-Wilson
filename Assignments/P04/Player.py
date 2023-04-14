from cmath import sqrt
import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self, default, sheet):
        self.offset = int(sqrt(len(sheet) - 1).real)

        self.__sprites = sheet
        
        #image -> player body
        #this is the main part of the sprite
        self.image = self.__sprites[default]
        self.rect = self.image.get_rect()
        self.rect.center = (10,10)
        
        self.head = self.__sprites[default - self.offset]
        self.headRec = self.head.get_rect()

    def draw(self, screen):
        self.rect.centerx += 1
        self.headRec.topleft = (self.rect.topleft[0], self.rect.topleft[1] - 16)

        screen.blit(self.image, self.rect)
        screen.blit(self.head, self.headRec)


        