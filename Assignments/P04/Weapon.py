import pygame
from cmath import sqrt
from Tile import Tile
from copy import deepcopy

class Weapon(pygame.sprite.Sprite):
    """ 
    Weapon class is a container for the weapon and its properties.

    Attributes
    ----------
    defaultSprite : int
        The default sprite
    offset : int
        The offset to the blade
    __sprites : list
        A list of sprites that the weapon will use  
    handle : Tile   
        The handle of the weapon    
    blade : Tile
        The blade of the weapon
    facing : str    
        The direction the weapon is facing

    Methods
    -------
    draw(screen, playerRec, playerFacing)
        Draws the weapon
    newWeapon(spriteNum)
        Changes the weapon
    getCollision(objectRecs, objectTiles, level, map)   
        Gets the collision of the weapon
    """
    def __init__(self, default, sheet, rec):
        """
        Constructor for Weapon class that takes in a sprite sheet.
        This creates the handle and blade of the weapon.

        Args:
            default (int): the default sprite number
            sheet (SpriteSheet): the sprite sheet
            rec (Rect): the rectangle of the weapon
        """
        self.defaultSprite = default
        self.offset = int(sqrt(len(sheet) - 1).real)
        self.__sprites = sheet
        handleRec = deepcopy(rec)
        handleRec.right += rec.width / 2
        self.handle = Tile(sheet[default], handleRec, default)
        bladeRec = deepcopy(rec)
        bladeRec.right += rec.width / 2 * 3
        self.blade = Tile(sheet[default - self.offset], bladeRec, default - self.offset)
        self.handle.image = pygame.transform.rotate(self.handle.image, -90)
        self.blade.image = pygame.transform.rotate(self.blade.image, -90)
        
        self.facing = 'R'

        
    def draw(self, screen, playerRec, playerFacing):
        """
        Draws the weapon.

        Args:
            screen (Surface): the screen to draw on
            playerRec (Rect): the rectangle of the player
            playerFacing (str): the direction the player is facing
        """
        self.handle.rect = deepcopy(playerRec)
        self.blade.rect = deepcopy(playerRec)
        
        if playerFacing == 'R':
            self.handle.rect.right += playerRec.width / 2
            self.blade.rect.right += playerRec.width / 2 * 3
            
            if self.facing != 'R':
                self.handle.image = pygame.transform.rotate(self.handle.image, 180)
                self.blade.image = pygame.transform.rotate(self.blade.image, 180)
                self.facing = 'R'
        elif playerFacing == 'L':
            self.handle.rect.right -= playerRec.width / 2
            self.blade.rect.right -= playerRec.width / 2 * 3
            
            if self.facing != 'L':
                self.handle.image = pygame.transform.rotate(self.handle.image, 180)
                self.blade.image = pygame.transform.rotate(self.blade.image, 180)
                self.facing = 'L'
            
        
        self.handle.draw(screen)
        self.blade.draw(screen)
    
    def newWeapon(self, spriteNum):
        """
        Changes the weapon.

        Args:
            spriteNum (int): the sprite number
        """
        self.defaultSprite = spriteNum
        
        self.blade.image = self.__sprites[spriteNum - self.offset]
        self.handle.image = self.__sprites[spriteNum]
        if self.facing == 'R':
            self.handle.image = pygame.transform.rotate(self.handle.image, -90)
            self.blade.image = pygame.transform.rotate(self.blade.image, -90)
        else:
            self.handle.image = pygame.transform.rotate(self.handle.image, 90)
            self.blade.image = pygame.transform.rotate(self.blade.image, 90)
            
    def getCollision(self, objectRecs, objectTiles, level, map):
        """
        Gets the collision of the weapon.

        Args:
            objectRecs (List[Rects]): the list of object rectangles
            objectTiles (list[Tiles]): the list of object tiles
            level (Level): the level the player is on
            map (Map): the map the player is on

        Returns:
            Bool: True if the weapon hits a goblin, False otherwise
        """
        weaponCollisions = self.blade.rect.collidelistall(objectRecs)
        weaponCollisions.extend(self.blade.rect.collidelistall(objectRecs))
        
        weaponCollisions = [*set(weaponCollisions)]
        
        if weaponCollisions == []:
            return False
        else:
            for collision in weaponCollisions:
                if objectTiles[collision].isLever():
                    level.leverEvent(objectTiles, collision)
                    
                elif objectTiles[collision].isGoblin():
                    if map.hitGoblin(objectTiles[collision]):
                        return True
            return False