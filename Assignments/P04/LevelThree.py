import pygame

class LevelThree:
    """
    The class for the third level and its logic.

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
    __leverTopR : int   
        The top right lever
    __leverTopL : int
        The top left lever
    __leverBottomR : int    
        The bottom right lever
    __leverBottomL : int    
        The bottom left lever
    __leverTopCurL : str    
        The current state of the top left lever
    __leverTopCurR : str
        The current state of the top right lever
    __leverBottomCurR : str
        The current state of the bottom right lever
    __leverBottomCurL : str
        The current state of the bottom left lever  
    __doorTopL : list   
        The top left door
    __doorTopR : list
        The top right door
    __doorBottomR : list    
        The bottom right door
    __doorBottomL : list
        The bottom left door
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
        
        
        pygame.mixer.music.load("Assets/sounds/LevelThree.wav")
        pygame.mixer.music.set_volume(.02)
        pygame.mixer.music.play()
        
        
        self.sheet = sheet.getSpritesList()
        self.__portalButtonTop = 301
        self.__portalButtonBottom = 844
        self.__portalLocation = portalLoc.rect.topleft
        self.__leverTopR = 305
        self.__leverTopL = 218
        self.__leverBottomR = 848
        self.__leverBottomL = 761
        self.__leverTopCurL = 'L'
        self.__leverTopCurR = 'L'
        self.__leverBottomCurR = 'L'  
        self.__leverBottomCurL = 'L'
        self.__doorTopL = [193,194,172,173]
        self.__doorTopR = [282,283,260,261]
        self.__doorBottomR = [825,826,803,804]
        self.__doorBottomL = [736,737,715,716]
        self.__doorOpen = pygame.mixer.Sound("Assets/sounds/open-doors.wav")
        self.__doorClose = pygame.mixer.Sound("Assets/sounds/door-close.wav")  
        
        self.__topObjs = 514
        
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
            _type_: _description_
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
        
        if objNum == self.__leverTopR:
            if self.__leverTopCurR == 'L':
                self.__leverTopCurR = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.set_volume(.3)
                self.__doorOpen.play()
                for part in self.__doorTopR:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverTopCurR = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.set_volume(.3)
                self.__doorClose.play()
                for part in self.__doorTopR:
                    tiles[part].updateState(self.__sheet, -3)
                    
        elif objNum == self.__leverTopL:
            if self.__leverTopCurL == 'L':
                self.__leverTopCurL = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.set_volume(.3)
                self.__doorOpen.play()
                for part in self.__doorTopL:
                    tiles[part].updateState(self.__sheet, 3)
                    
            else:
                self.__leverTopCurL = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.set_volume(.3)
                self.__doorClose.play()
                for part in self.__doorTopL:
                    tiles[part].updateState(self.__sheet, -3)
               
                    
        elif objNum == self.__leverBottomR:
            if self.__leverBottomCurR == 'L':
                self.__leverBottomCurR = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.set_volume(.3)
                self.__doorOpen.play()
                for part in self.__doorBottomR:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverBottomCurR = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.set_volume(.3)
                self.__doorClose.play()
                for part in self.__doorBottomR:
                    tiles[part].updateState(self.__sheet, -3)
                    
        elif objNum == self.__leverBottomL:
            if self.__leverBottomCurL == 'L':
                self.__leverBottomCurL = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.set_volume(.3)
                self.__doorOpen.play()
                for part in self.__doorBottomL:
                    tiles[part].updateState(self.__sheet, 3)
                    
            else:
                self.__leverBottomCurL = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.set_volume(.3)
                self.__doorClose.play()
                for part in self.__doorBottomL:
                    tiles[part].updateState(self.__sheet, -3)
                
        

    def getTopObjs(self):
        """
        Returns the number of objects on the top layer.

        Returns:
            int: the number of objects on the top layer
        """
        return self.__topObjs