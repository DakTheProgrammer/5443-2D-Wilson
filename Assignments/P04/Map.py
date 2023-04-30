import pygame
from pathlib import Path
import pytiled_parser
from PIL import Image

from Goblin import Goblin
from Tile import Tile

class Map:
    def __init__(self, tmx, sheet):
        file = Path(tmx)
        mapInfo = pytiled_parser.parse_map(file)

        tileSize = mapInfo.tile_size[0]
                
        floorCSV = mapInfo.layers[0].data
        objectsCSV = mapInfo.layers[1].data
        
        self.__tileImages = sheet
        self.__floorTiles = []
        self.__objectTiles = []
        self.__objectRecs = []
        self.__objects = []
        self.__players = []

        self.__goblins = []

        self.__oneGoblinsSprites = [184]
        self.__twoGoblinsSprites = [[664,696]]
        self.__fourGoblinsSprites = [[738,739,770,771]]
        
        self.__twoHolder = []
        self.__fourHolder = []
        
        self.__loadTiles(floorCSV, objectsCSV, tileSize)
        
        for object in self.__objectTiles:
            if object.getTileNum() != 0:
                self.__objectRecs.append(object.rect)
                self.__objects.append(object)
        
    def draw(self, screen):
        for goblin in self.__goblins:
            goblin.getCollisions(self.__objectRecs, self.__objects)
            goblin.move()

        for tile in self.__floorTiles:
            tile.draw(screen)
            
        for tile in self.__objectTiles:
            if tile.isCoin() and tile.animationBuffer == tile.maxBuffer:
                tile.animationBuffer = 0
                if tile.getTileNum() == 563:
                    tile.update(564, self.__tileImages[564])
                else:
                    tile.update(563, self.__tileImages[563])
            else:
                tile.animationBuffer += 1
                
            tile.draw(screen)
            # for gob in self.__goblins:
            #     pygame.draw.rect(screen, (255,0,0), gob.rect)

    def getTileset(self):
        return self.__tileImages
    
    def __loadTiles(self, floor, objects, size):
        for i, list in enumerate(floor):
            for j, num in enumerate(list):
                self.__floorTiles.append(Tile(self.__tileImages[num], (j * size, i * size, size, size),num))
                
        for i, list in enumerate(objects):
            for j, num in enumerate(list):
                self.__objectTiles.append(Tile(self.__tileImages[num], (j * size, i * size, size, size),num))
                
    def getSpawnTile(self):
        # self.__objectTiles.index(196)
        spawnPos = []
        for tile in self.__objectTiles:
            if tile.getTileNum() == 196:
                spawnPos.append(tile)
                if len(spawnPos) == 2:
                    return spawnPos
        return spawnPos
    
    def getObjectRecs(self):
        return self.__objectRecs
    
    def getObjects(self):
        return self.__objects

    def setPlayers(self, players):
        self.__players = players

        for object in self.__objectTiles:
            if object.getTileNum() in self.__oneGoblinsSprites:
                self.__goblins.append(Goblin([object], self.__players, self.__tileImages))
            else:
                for char in self.__twoGoblinsSprites:
                    if object.getTileNum() in char:
                        if object.getTileNum() == char[0]:
                            self.__twoHolder.append([object])
                        else:
                            self.__twoHolder[0].append(object)
                            self.__goblins.append(Goblin(self.__twoHolder[0], self.__players, self.__tileImages))
                            self.__twoHolder.pop(0)
                            
                for char in self.__fourGoblinsSprites:
                    if object.getTileNum() in char:
                        if object.getTileNum() == char[0]:
                            self.__fourHolder.append([object])
                        else:
                            index = char.index(object.getTileNum())
                            for holder in self.__fourHolder:
                                if len(holder) == index:
                                    holder.append(object)
                                    break
                            if self.__fourHolder != [] and len(self.__fourHolder[0]) == 4:
                                self.__goblins.append(Goblin(self.__fourHolder[0], self.__players, self.__tileImages))
                                self.__fourHolder.pop(0)
                                        
                  
                            
                    