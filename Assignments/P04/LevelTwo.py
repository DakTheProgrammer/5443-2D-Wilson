import pygame

class LevelTwo:
    """
    the level two class and its logic.

    Attributes
    ----------
    sheet : SpriteSheet
        The sprite sheet
    __portalButtonTop : int
        The top portal button
    __portalButtonBottom : int  
        The bottom portal button
    __portalLocation : tuple
        The location of the portal
    __leverTop : int
        The top lever
    __leverTopCur : str 
        The current state of the top lever
    __leverBottomCur : str  
        The current state of the bottom lever
    __doorTop : list    
        The top door
    __doorBottom : list
        The bottom door
    __doorOpen : Sound  
        The sound for opening the door
    __doorClose : Sound 
        The sound for closing the door
    __topObjs : int 
        The number of objects on the top layer
    __sheet : SpriteSheet   
        The sprite sheet

    Methods
    -------
    buttonEvent(objNum, tiles, bodySprite, weaponSprite)
        The event for the portal button
    leverEvent(tiles, objNum)
        The event for the lever
    getTopObjs()
        Returns the number of objects on the top layer
    """
    def __init__(self, sheet, portalLoc):
        """
        Constructor for LevelTwo class.

        Args:
            sheet (SpriteSheet): the sprite sheet
            portalLoc (tuple): the location of place to portal to
        """
      
        pygame.mixer.music.load("Assets/sounds/LevelTwo.wav")
        pygame.mixer.music.set_volume(.04)
        pygame.mixer.music.play()
        
        self.sheet = sheet.getSpritesList()
        self.__portalButtonTop = 51
        self.__portalButtonBottom = 300
        self.__portalLocation = portalLoc.rect.topleft
        self.__leverTop = 145
        self.__leverTopCur = 'L'
        self.__leverBottomCur = 'L'  
        self.__doorTop = [131,132,118,119]
        self.__doorBottom = [380,381,367,368]
        self.__doorOpen = pygame.mixer.Sound("Assets/sounds/open-doors.wav")
        self.__doorClose = pygame.mixer.Sound("Assets/sounds/door-close.wav")
        self.__topObjs = 229
    
        self.__sheet = sheet
        
    def buttonEvent(self, objNum, tiles, bodySprite, weaponSprite):
        """
        The event for the portal button.

        Args:
            objNum (int): the object number
            tiles (list): the list of tiles
            bodySprite (Body): the body sprite
            weaponSprite (Weapon): the weapon sprite

        Returns:
            tuple: the location of the portal and that the type is a portal
        """
        if objNum == self.__portalButtonBottom:
            tiles[self.__portalButtonBottom].update(389, self.sheet[389])
        else:
            tiles[self.__portalButtonTop].update(389, self.sheet[389])

        return self.__portalLocation, 'P'
        
    def leverEvent(self, tiles, objNum):
        """
        The event for the lever.

        Args:
            tiles (list): the list of tiles
            objNum (int): the object number
        """
        if objNum == self.__leverTop:
            if self.__leverTopCur == 'L':
                self.__leverTopCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.set_volume(.3)
                self.__doorOpen.play()
                for part in self.__doorTop:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverTopCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.set_volume(.3)
                self.__doorClose.play()
                for part in self.__doorTop:
                    tiles[part].updateState(self.__sheet, -3)
        else:
            if self.__leverBottomCur == 'L':
                self.__leverBottomCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.set_volume(.3)
                self.__doorOpen.play()
                for part in self.__doorBottom:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverBottomCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.set_volume(.3)
                self.__doorClose.play()
                for part in self.__doorBottom:
                    tiles[part].updateState(self.__sheet, -3)

    def getTopObjs(self):
        """
        Returns the number of objects on the top layer.

        Returns:
            int: the number of objects on the top layer
        """
        return self.__topObjs