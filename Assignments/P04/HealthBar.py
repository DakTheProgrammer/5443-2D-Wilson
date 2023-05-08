import pygame
from Tile import Tile
# 531: full, 532: half, 533: empty
class HealthBar:
    """
    HealthBar class is a container for the health bar.

    Attributes
    ----------
    sheet : SpriteSheet
        The sprite sheet
    tiles : list
        A list of tiles that the health bar will use
    scale : tuple
        The scale of the health bar

    Methods
    -------
    draw(screen, left, top)
        Draws the health bar
    update(health)
        Updates the health bar
    """
    def __init__(self, sheet):
        """
        Constructor for HealthBar class that takes in a sprite sheet.

        Args:
            sheet (SpriteSheet): The sprite sheet
        """
        self.sheet = sheet
        self.tiles = []

        self.scale = (32,32)

        for i in range(5):
            self.tiles.append(Tile(sheet[531],pygame.rect.Rect(i*self.scale[0],0,self.scale[0],self.scale[0]),531))
        
            self.tiles[i].image = pygame.transform.scale(self.tiles[i].image, self.scale)
            
    def draw(self, screen, left, top):
        """
        Draws the health bar.

        Args:
            screen (Surface): The screen to draw on
            left (int): The left side of the screen
            top (int): The top of the screen
        """
        for i, tile in enumerate(self.tiles):
            tile.rect.topleft = (left + (i * self.scale[0]), top)
            screen.blit(tile.image, tile.rect)
    
    def update(self, health):
        """
        Updates the health bar.

        Args:
            health (int): the health of the player
        """
        for i in range(len(self.tiles)):
            if health >= 20 + (i * 20):
                self.tiles[i].image = pygame.transform.scale(self.sheet[531], self.scale)
            elif health > i * 20:
                self.tiles[i].image = pygame.transform.scale(self.sheet[532], self.scale)
            else:
                self.tiles[i].image = pygame.transform.scale(self.sheet[533], self.scale)
