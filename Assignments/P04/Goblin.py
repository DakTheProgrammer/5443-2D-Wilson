import pygame
import math

class Goblin:
    def __init__(self, tiles, players, sheet):
        self.sheet = sheet
        self.tiles = tiles

        dist = 10000

        self.closestPlayer = None

        for player in players:
            if math.dist(tiles.rect.topleft, player.rect.topleft) < dist:
                dist = math.dist(tiles.rect.topleft, player.rect.topleft)
                self.closestPlayer = player

        self.moveDelay = 0
        self.maxMoveDelay = 3

        self.default = self.tiles.getTileNum()
        self.animationNum = 0
        self.maxAnimation = 7

    def move(self):
        if self.moveDelay == self.maxMoveDelay:
            
            if self.animationNum != self.maxAnimation:
                self.tiles.update(self.tiles.getTileNum() + 1, self.sheet[self.tiles.getTileNum() + 1])
                self.animationNum += 1
            else:
                self.animationNum = 0
                self.tiles.update(self.default, self.sheet[self.default])

            
            self.moveDelay = 0
            
            if self.tiles.rect[0] != self.closestPlayer.rect[0]:
                if self.tiles.rect[0] < self.closestPlayer.rect[0]:
                    self.tiles.rect[0] += 1
                else:
                    self.tiles.rect[0] -= 1
            
            if self.tiles.rect[1] != self.closestPlayer.rect[1]:
                if self.tiles.rect[1] < self.closestPlayer.rect[1]:
                    self.tiles.rect[1] += 1
                else:
                    self.tiles.rect[1] -= 1
        else:
            self.moveDelay += 1

        