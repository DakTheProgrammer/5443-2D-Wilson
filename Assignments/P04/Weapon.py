import pygame
from cmath import sqrt
from Tile import Tile
from copy import deepcopy

class Weapon(pygame.sprite.Sprite):
    def __init__(self, default, sheet, rec):
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