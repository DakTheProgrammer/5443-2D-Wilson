import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, img, rect, index):
        self.image = img
        self.rect = pygame.rect.Rect(rect)
        self.__tileNum = index
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def getTileNum(self):
        return self.__tileNum
        