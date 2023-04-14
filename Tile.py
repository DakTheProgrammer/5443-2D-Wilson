import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, img, rect):
        self.image = img
        self.rect = rect
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        
        