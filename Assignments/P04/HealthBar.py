import pygame
from Tile import Tile
# 531: full, 532: half, 533: empty
class HealthBar:
    def __init__(self, sheet):
        self.tiles = []

        self.scale = (32,32)

        for i in range(5):
            self.tiles.append(Tile(sheet[531],pygame.rect.Rect(i*self.scale[0],0,self.scale[0],self.scale[0]),531))
        
            self.tiles[i].image = pygame.transform.scale(self.tiles[i].image, self.scale)
            
    def draw(self, screen, left, top):
        for i, tile in enumerate(self.tiles):
            tile.rect.topleft = (left + (i * self.scale[0]), top)
            screen.blit(tile.image, tile.rect)