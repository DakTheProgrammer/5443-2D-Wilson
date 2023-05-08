import pygame
import  pytiled_parser
from pathlib import Path
from PIL import Image

class SpriteSheet:
    """
    SpriteSheet class is a container for the sprite sheet and its properties.

    Attributes
    ----------
    __tileImages : list
        A list of tiles that the sprite sheet will use
    
    Methods
    -------
    getSpritesList()
        Gets the list of tiles
    """
    def __init__(self, tmx):
        """
        Constructor for SpriteSheet class that takes in a tmx file.

        Args:
            tmx (str): the tmx file name
        """
        file = Path(tmx)
        mapInfo = pytiled_parser.parse_map(file)
        
        sheet = Image.open(str(mapInfo.tilesets[1].image)[1:])
        tileSize = mapInfo.tile_size[0]
        
        #columns = rows
        columns = mapInfo.tilesets[1].columns
        
        self.__tileImages = []
        
        #places a transparent tile in spot 0
        alphaBlock = sheet.crop((0,0,tileSize, tileSize))
        self.__tileImages.append(pygame.image.fromstring(alphaBlock.tobytes(), alphaBlock.size, alphaBlock.mode))
        
        for r in range(columns):
            for c in range(columns):
                img = sheet.crop(((c * tileSize), (r * tileSize), tileSize * (c + 1), tileSize + (tileSize * r)))
                
                self.__tileImages.append(pygame.image.fromstring(img.tobytes(), img.size, img.mode))

    def getSpritesList(self):
        """
        gets the list of tiles

        Returns:
            list: the list of tiles
        """
        return self.__tileImages