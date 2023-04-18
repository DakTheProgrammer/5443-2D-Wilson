import pygame
from pathlib import Path
import pytiled_parser
from PIL import Image

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
        
        self.__loadTiles(floorCSV, objectsCSV, tileSize)
        
        for object in self.__objectTiles:
            if object.getTileNum() != 0:
                self.__objectRecs.append(object.rect)
                self.__objects.append(object)
        
    def draw(self, screen):
        for tile in self.__floorTiles:
            tile.draw(screen)
            
        for tile in self.__objectTiles:
            tile.draw(screen)

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