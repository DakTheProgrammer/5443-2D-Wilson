import pygame
from pathlib import Path
import pytiled_parser
from PIL import Image

from Tile import Tile

class Map:
    def __init__(self, tmx):
        file = Path(tmx)
        mapInfo = pytiled_parser.parse_map(file)
        
        sheet = Image.open(str(mapInfo.tilesets[1].image)[1:])
        tileSize = mapInfo.tile_size[0]
        
        #columns = rows
        columns = mapInfo.tilesets[1].columns
        
        self.tileImages = []
        
        #places a tranparent tile in spot 0
        alphaBlock = sheet.crop((0,0,tileSize, tileSize))
        self.tileImages.append(pygame.image.fromstring(alphaBlock.tobytes(), alphaBlock.size, alphaBlock.mode))
        
        for r in range(columns):
            for c in range(columns):
                img = sheet.crop(((c * tileSize), (r * tileSize), tileSize * (c + 1), tileSize + (tileSize * r)))
                
                self.tileImages.append(pygame.image.fromstring(img.tobytes(), img.size, img.mode))
                
        floorCSV = mapInfo.layers[0].data
        objectsCSV = mapInfo.layers[1].data
        
        self.floorTiles = []
        self.objectTiles = []
        
        self.__loadTiles(floorCSV, objectsCSV, tileSize)
        
    def draw(self, screen):
        for tile in self.floorTiles:
            tile.draw(screen)
            
        for tile in self.objectTiles:
            tile.draw(screen)
    
    def __loadTiles(self, floor, objects, size):
        for i, list in enumerate(floor):
            for j, num in enumerate(list):
                self.floorTiles.append(Tile(self.tileImages[num], (j * size, i * size, size, size)))
                
        for i, list in enumerate(objects):
            for j, num in enumerate(list):
                self.objectTiles.append(Tile(self.tileImages[num], (j * size, i * size, size, size)))