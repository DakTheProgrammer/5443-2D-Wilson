from cmath import sqrt
import pygame
from Weapon import Weapon
class Player(pygame.sprite.Sprite):
    
    def __init__(self, default, sheet, spawn):
        
        self.weapon = Weapon(340,sheet)
        self.offset = int(sqrt(len(sheet) - 1).real)
        self.__sprites = sheet
        
        #image -> player body
        #this is the main part of the sprite
        self.image = self.__sprites[default]
        self.rect = self.image.get_rect()
        self.rect.topleft = spawn.rect.topleft
        
        self.head = self.__sprites[default - self.offset]
        self.headRec = self.head.get_rect()
        self.currentFrame = 0
        self.walking = [self.__sprites[default], self.__sprites[default+1], self.__sprites[default+2], self.__sprites[default+3]]
        
        self.moveSpeed = 1
        self.facing = 'R'

    def draw(self, screen):
        self.headRec.topleft = (self.rect.topleft[0], self.rect.topleft[1] - self.rect.height)

        screen.blit(self.image, self.rect)
        screen.blit(self.head, self.headRec)
        
    #  -y moves up, +y moves down, -x moves left, +x moves right
    def move(self, x, y):
        if x != 0 or y != 0:
            if self.currentFrame == len(self.walking) - 1:
                self.currentFrame = 0
            else:
                self.currentFrame += 1
                self.image = self.walking[self.currentFrame]
                if self.facing == 'L':
                    self.image = pygame.transform.flip(self.image, True, False)
            
            if self.facing == 'R' and x < 0:
                self.facing = 'L'
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.facing == 'L' and x > 0:
                self.facing = 'R'    
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect.left += x * self.moveSpeed
            self.rect.top += y * self.moveSpeed