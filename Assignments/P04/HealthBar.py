import pygame
from Tile import Tile
# 531: full, 532: half, 533: empty
class HealthBar:
    def __init__(self, sheet):
        self.tiles = []
        for i in range(5):
            self.tiles.append(Tile(sheet[531],pygame.rect.Rect(i*16,0,16,16),531))
            
    def draw(self, screen, left, top):
        for i, tile in enumerate(self.tiles):
            tile.rect.topleft = (left + (i * 16), top)
            screen.blit(tile.image, tile.rect)