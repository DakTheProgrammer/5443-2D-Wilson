from pathlib import Path
import pytiled_parser
import pygame
from Goblin import Goblin
from Tile import Tile

class Map:
    """
    This class is used to load the map from a tmx file and create the tiles
    for the map.

    Attributes
    ----------
    __tileImages : list
        The list of tile images
    __floorTiles : list
        The list of floor tiles
    __objectTiles : list
        The list of object tiles
    __objectRecs : list
        The list of object rectangles
    __objects : list    
        The list of objects
    __players : list
        The list of players
    __goblins : list
        The list of goblins
    __oneGoblinsSprites : list
        The list of one goblin sprites
    __twoGoblinsSprites : list
        The list of two goblin sprites
    __fourGoblinsSprites : list 
        The list of four goblin sprites
    __twoHolder : list  
        The list of two goblin holders
    __fourHolder : list
        The list of four goblin holders
    
    Methods
    -------
    draw(screen)
        Draws the map
    getTileset()
        Returns the tileset
    __loadTiles(floor, objects, size)
        Loads the tiles
    getSpawnTile()
        Returns the spawn tile
    getPortalTile()
        Returns the portal tile
    getObjectRecs()
        Returns the object rectangles
    """
    def __init__(self, tmx, sheet):
        """
        Constructor for Map class that loads the map from a tmx file and creates the tiles.

        Args:
            tmx (str): the tmx file
            sheet (SpriteSheet): the sprite sheet
        """
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
        self.__oneGoblinsSprites = [56,88,120,184,248,312]
        self.__twoGoblinsSprites = [[664,696],[600,632],[472,504],[344,376]]
        self.__fourGoblinsSprites = [[738,739,770,771],[546,547,578,579],[642,643,674,675]]
        
        self.__twoHolder = []
        self.__fourHolder = []
        
        self.__loadTiles(floorCSV, objectsCSV, tileSize)
        
        for object in self.__objectTiles:
            if object.getTileNum() != 0:
                self.__objectRecs.append(object.rect)
                self.__objects.append(object)
        
    def draw(self, screen):
        """
        Draws the map.

        Args:
            screen (Surface): the display surface
        """
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
            elif tile.isCoin():
                tile.animationBuffer += 1
            
            if tile.isNPC() and tile.animationBuffer == tile.maxBuffer:
                tile.animationBuffer = 0
                if  tile.getTileNum() < 766:
                    tile.update(tile.getTileNum()+1, self.__tileImages[tile.getTileNum()+1])
                else:
                    tile.update(760, self.__tileImages[760])
            elif tile.isNPC():
                tile.animationBuffer += 1
            
            if (tile.isTrap() or tile.getTileNum() == 354) and tile.animationBuffer == tile.maxTrapBuffer:
                tile.animationBuffer = 0
                if tile.getTileNum() == 357:
                    tile.update(356, self.__tileImages[356])
                elif tile.getTileNum() == 356:
                    tile.update(355, self.__tileImages[355])
                elif tile.getTileNum() == 355:
                    tile.update(354, self.__tileImages[354])
                else: 
                    tile.update(357, self.__tileImages[357])
            elif tile.isTrap() or tile.getTileNum() == 354:
                tile.animationBuffer += 1
          
            tile.draw(screen)

            # for gob in self.__goblins:
            #     pygame.draw.rect(screen, (255,0,0), gob.rect)

            
            
    def getTileset(self):
        """
        Returns the tileset.

        Returns:
            list: the tileset
        """
        return self.__tileImages
    
    def __loadTiles(self, floor, objects, size):
        """
        Loads the tiles.

        Args:
            floor (list): the floor tiles
            objects (list): the object tiles
            size (int): the size of the tiles
        """
        for i, list in enumerate(floor):
            for j, num in enumerate(list):
                self.__floorTiles.append(Tile(self.__tileImages[num], (j * size, i * size, size, size),num))
                
        for i, list in enumerate(objects):
            for j, num in enumerate(list):
                self.__objectTiles.append(Tile(self.__tileImages[num], (j * size, i * size, size, size),num))
                
    def getSpawnTile(self):
        """
        Returns the spawn tile.

        Returns:
            list: the spawn tile
        """
        spawnPos = []
        for tile in self.__objectTiles:
            if tile.getTileNum() == 196:
                spawnPos.append(tile)
                if len(spawnPos) == 2:
                    return spawnPos
        return spawnPos
    
    def getPortalTile(self):
        """
        Returns the portal tile.

        Returns:
            list: the portal tile
        """
        portalPos = []
        for tile in self.__objectTiles:
            if tile.getTileNum() == 295:
                portalPos.append(tile)
                if len(portalPos) == 2:
                    return portalPos
        return portalPos
    
    def getObjectRecs(self):
        """
        Returns the object rectangles.

        Returns:
            list: the object rectangles
        """
        return self.__objectRecs
    
    def getObjects(self):
        """
        Returns the objects.

        Returns:
            list: the objects
        """
        return self.__objects

    def setPlayers(self, players):
        """
        Sets the players.

        Args:
            players (list[Player]): the players
        """
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
                                        
    def hitGoblin(self, tile):
        """
        Hits the goblin.

        Args:
            tile (Tile): the tile

        Returns:
            bool: whether the goblin was hit
        """
        for goblin in self.__goblins:
            if tile in goblin.tiles:
                goblin.hit(self.__tileImages)
                if goblin.goblinHealth == 0:
                    self.__goblins.remove(goblin)
                    return True        
        return False