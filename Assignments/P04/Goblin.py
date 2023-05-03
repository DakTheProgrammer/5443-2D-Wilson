import pygame
import math

class Goblin:
    def __init__(self, tiles, players, sheet):
        self.sheet = sheet
        self.tiles = tiles
        if len(self.tiles) == 1:
            self.rect = pygame.rect.Rect(self.tiles[0].rect.topleft, (16, 16))
            self.goblinHealth = 1
        elif len(self.tiles) == 2:
            self.rect = pygame.rect.Rect(self.tiles[0].rect.topleft, (16, 32))
            self.goblinHealth = 2
        else:
            self.rect = pygame.rect.Rect(self.tiles[0].rect.topleft, (32, 32))
            self.goblinHealth = 4
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
        
        self.__canMove = {
            'Up': True,
            'Down': True,
            'Right': True,
            'Left': True
        }
        
        self.defaults = []
        for tile in self.tiles:
            self.defaults.append(tile.getTileNum())
            
        self.animationNum = 0
        self.maxAnimation = 7
        self.alive = True

    def move(self):
        if self.alive and self.tiles[0].getTileNum() == 0:
            self.alive = False

        if self.alive:
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
                            if tile.rect[0] < self.closestPlayer.rect[0] and self.__canMove['Right']:
                                tile.rect[0] += self.moveSpeed
                                x = self.moveSpeed
                            elif self.__canMove['Left']:
                                tile.rect[0] -= self.moveSpeed
                                x = -self.moveSpeed
                        
                        if tile.rect[1] != self.closestPlayer.rect[1]:
                            if tile.rect[1] < self.closestPlayer.rect[1] and self.__canMove['Down']:
                                tile.rect[1] += self.moveSpeed
                                y = self.moveSpeed
                            elif self.__canMove['Up']:
                                tile.rect[1] -= self.moveSpeed
                                y = -self.moveSpeed
                    else:
                        tile.rect[0] += x
                        tile.rect[1] += y
                        
                self.rect[0] += x
                self.rect[1] += y
            else:
                self.moveDelay += 1
                
            self.__canMove = {
                    'Up': True,
                    'Down': True,
                    'Right': True,
                    'Left': True
                }
        

    def getCollisions(self, objectRecs, objectTiles):
        goblinCollisions = self.rect.collidelistall(objectRecs)
        if goblinCollisions == []:
            return False
        else:
            for collision in goblinCollisions:
                if objectTiles[collision].isBarrier():
                    
                    
                    angle = self.__angle_of_line(self.rect.centerx, self.rect.centery, objectRecs[collision].centerx, objectRecs[collision].centery)
                        
                        #use to test for my bad trig
                        #print(angle)

                    if angle > -45 and angle < 45:
                        self.__canMove['Right'] = False
                    
                    if (angle > 135 and angle <= 180) or (angle > -180 and angle < -135):
                        self.__canMove['Left'] = False
                    
                    if angle < -45 and angle > -135:
                        self.__canMove['Down'] = False

                    if angle > 45 and angle < 135:
                        self.__canMove['Up'] = False
                        
    def hit(self, sheet):
        self.goblinHealth -= 1
        if self.goblinHealth == 0:
            for tile in self.tiles:
                tile.update(0, sheet[0])

                        
    def __angle_of_line(self, x1, y1, x2, y2):
        return math.degrees(math.atan2(-(y2-y1), x2-x1))
    
    
