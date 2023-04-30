import pygame
import math

class Goblin:
    def __init__(self, tiles, players, sheet):
        self.sheet = sheet
        self.tiles = tiles
        self.rect = pygame.rect.Rect(self.tiles[0].rect.topleft, (16, 16))
        self.tiles.reverse()

        dist = 10000

        self.closestPlayer = None

        for player in players:
            if math.dist(tiles[0].rect.topleft, player.rect.topleft) < dist:
                dist = math.dist(tiles[0].rect.topleft, player.rect.topleft)
                self.closestPlayer = player
        self.moveSpeed = 1
        self.moveDelay = 0
        self.maxMoveDelay = 3

        self.defaults = []
        for tile in self.tiles:
            self.defaults.append(tile.getTileNum())
            
        self.animationNum = 0
        self.maxAnimation = 7

    def move(self):
        if self.moveDelay == self.maxMoveDelay:
            
            if self.animationNum != self.maxAnimation:
                for tile in self.tiles:
                    if len(self.tiles) < 3:
                        tile.update(tile.getTileNum() + 1, self.sheet[tile.getTileNum() + 1])
                    else:
                        tile.update(tile.getTileNum() + 2, self.sheet[tile.getTileNum() + 2])
                self.animationNum += 1
            else:
                self.animationNum = 0
                for i, tile in enumerate(self.tiles):
                    tile.update(self.defaults[i], self.sheet[self.defaults[i]])

            
            self.moveDelay = 0
            
            x,y = 0,0
            
            for i,tile in enumerate(self.tiles):
                if i == 0:
                    if tile.rect[0] != self.closestPlayer.rect[0]:
                        if tile.rect[0] < self.closestPlayer.rect[0]:
                            tile.rect[0] += self.moveSpeed
                            x = self.moveSpeed
                        else:
                            tile.rect[0] -= self.moveSpeed
                            x = -self.moveSpeed
                    
                    if tile.rect[1] != self.closestPlayer.rect[1]:
                        if tile.rect[1] < self.closestPlayer.rect[1]:
                            tile.rect[1] += self.moveSpeed
                            y = self.moveSpeed
                        else:
                            tile.rect[1] -= self.moveSpeed
                            y = -self.moveSpeed
                else:
                    tile.rect[0] += x
                    tile.rect[1] += y
                    
            self.rect[0] += x
            self.rect[1] += y
        else:
            self.moveDelay += 1
        

    def getCollisions(self, objectRecs, objectTiles):
        goblinCollisions = self.rect.collidelistall(objectRecs)
        if goblinCollisions == []:
            return False
        else:
            for collision in goblinCollisions:
                if objectTiles[collision].isBarrier():
                    
                    self.moveSpeed = 0
