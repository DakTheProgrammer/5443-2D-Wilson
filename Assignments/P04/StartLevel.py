import pygame
from cmath import sqrt

class StartLevel:
    """
    StartLevel class is a container for the start level.

    Attributes
    ----------
    __redCharSelectButtons : list
        A list of red character select buttons
    __blueCharSelectButtons : list
        A list of blue character select buttons
    __redWeaponSelectButtons : list
        A list of red weapon select buttons
    __blueWeaponSelectButtons : list
        A list of blue weapon select buttons
    __redCharSelectButtonsCur : int
        The current red character select button
    __blueCharSelectButtonsCur : int
        The current blue character select button
    __redWeaponSelectButtonsCur : int
        The current red weapon select button
    __blueWeaponSelectButtonsCur : int
        The current blue weapon select button
    __newBodyOffset : int
        The new body location offset
    __newHeadOffset : int
        The new head location offset
    __leverTop : int
        The top lever
    __leverBottom : int
        The bottom lever
    __leverTopCur : str
        The current top lever state
    __leverBottomCur : str
        The current bottom lever state
    __doorOpen : pygame.mixer.Sound
        A sound that plays when the door opens
    __doorClose : pygame.mixer.Sound
        A sound that plays when the door closes
    __doorTop : list
        A list of the top door parts
    __doorBottom : list
        A list of the bottom door parts
    __topObjs : int
        The number of top objects
    __spriteOffset : int
        The sprite offset
    __sheet : SpriteSheet
        The sprite sheet
    
    Methods
    -------
    buttonEvent(objNum, tiles, bodySprite, weaponSprite)
        Handles button events
    leverEvent(tiles, objNum)
        Handles lever events
    getTopObjs()
        Gets the number of top objects
    """
    def __init__(self, sheet):
        """
        Constructor for StartLevel class that takes in a sprite sheet.
        To handle all the level states.

        Args:
            sheet (SpriteSheet): the sprite sheet
        """
       
        pygame.mixer.music.load("Assets/sounds/StartLevel.wav")
        pygame.mixer.music.set_volume(.05)
        pygame.mixer.music.play()
    
        self.__redCharSelectButtons = [117,118,119,120]
        self.__blueCharSelectButtons = [278, 279, 280, 281]
        self.__redWeaponSelectButtons = [114,115,116]
        self.__blueWeaponSelectButtons = [275, 276, 277]
        self.__redCharSelectButtonsCur = 120
        self.__blueCharSelectButtonsCur = 281
        self.__redWeaponSelectButtonsCur = 116
        self.__blueWeaponSelectButtonsCur = 277
        self.__newBodyOffset = 18
        self.__newHeadOffset = 9
        self.__leverTop = 84
        self.__leverBottom = 245
        self.__leverTopCur = 'L'
        self.__leverBottomCur = 'L'
        self.__doorOpen = pygame.mixer.Sound("Assets/sounds/open-doors.wav")
        self.__doorClose = pygame.mixer.Sound("Assets/sounds/door-close.wav")
        
        self.__doorTop = [73,72,55,54]
        self.__doorBottom = [234,233,216,215]

        self.__topObjs = 142
        
        self.__spriteOffset = int(sqrt(len(sheet.getSpritesList()) - 1).real)
        
        self.__sheet = sheet

    def buttonEvent(self, objNum, tiles, bodySprite, weaponSprite):
        """
        Handles button events.

        Args:
            objNum (int): the object number for the button
            tiles (List): the list of tiles to update
            bodySprite (Tile): the body sprite to update
            weaponSprite (Tile): the weapon sprite to update

        Returns:
            sprite, key: a tuple of the sprite and key
        """
        if objNum in self.__redCharSelectButtons:
            tiles[self.__redCharSelectButtonsCur - self.__newBodyOffset].update(bodySprite, self.__sheet.getSpritesList()[bodySprite])
            tiles[self.__redCharSelectButtonsCur - self.__newBodyOffset - self.__newHeadOffset].update(bodySprite - self.__spriteOffset, self.__sheet.getSpritesList()[bodySprite - self.__spriteOffset])

            
            tiles[objNum].updateState(self.__sheet, 1)
            tiles[self.__redCharSelectButtonsCur].updateState(self.__sheet, -1)

            self.__redCharSelectButtonsCur = objNum

            body = tiles[objNum - self.__newBodyOffset].getTileNum()
            
            tiles[objNum - self.__newBodyOffset].update(1, self.__sheet.getSpritesList()[1])
            tiles[objNum - self.__newBodyOffset - self.__newHeadOffset].update(1, self.__sheet.getSpritesList()[1])
            
            return body, 'B'
        
        elif objNum in self.__blueCharSelectButtons:
            tiles[self.__blueCharSelectButtonsCur - self.__newBodyOffset].update(bodySprite, self.__sheet.getSpritesList()[bodySprite])
            tiles[self.__blueCharSelectButtonsCur - self.__newBodyOffset - self.__newHeadOffset].update(bodySprite - self.__spriteOffset, self.__sheet.getSpritesList()[bodySprite - self.__spriteOffset])

            
            tiles[objNum].updateState(self.__sheet, 1)
            tiles[self.__blueCharSelectButtonsCur].updateState(self.__sheet, -1)

            self.__blueCharSelectButtonsCur = objNum

            body = tiles[objNum - self.__newBodyOffset].getTileNum()
            
            tiles[objNum - self.__newBodyOffset].update(1, self.__sheet.getSpritesList()[1])
            tiles[objNum - self.__newBodyOffset - self.__newHeadOffset].update(1, self.__sheet.getSpritesList()[1])
            
            return body, 'B'
        
        elif objNum in self.__redWeaponSelectButtons:
            tiles[self.__redWeaponSelectButtonsCur - self.__newBodyOffset].update(weaponSprite, self.__sheet.getSpritesList()[weaponSprite])
            tiles[self.__redWeaponSelectButtonsCur - self.__newBodyOffset - self.__newHeadOffset].update(weaponSprite - self.__spriteOffset, self.__sheet.getSpritesList()[weaponSprite - self.__spriteOffset])

            tiles[objNum].updateState(self.__sheet, 1)
            tiles[self.__redWeaponSelectButtonsCur].updateState(self.__sheet, -1)
            
            self.__redWeaponSelectButtonsCur = objNum
            body = tiles[objNum - self.__newBodyOffset].getTileNum()
            
            tiles[objNum - self.__newBodyOffset].update(1, self.__sheet.getSpritesList()[1])
            tiles[objNum - self.__newBodyOffset - self.__newHeadOffset].update(1, self.__sheet.getSpritesList()[1])
            
            return body, 'W'
        
        elif objNum in self.__blueWeaponSelectButtons:
            tiles[self.__blueWeaponSelectButtonsCur - self.__newBodyOffset].update(weaponSprite, self.__sheet.getSpritesList()[weaponSprite])
            tiles[self.__blueWeaponSelectButtonsCur - self.__newBodyOffset - self.__newHeadOffset].update(weaponSprite - self.__spriteOffset, self.__sheet.getSpritesList()[weaponSprite - self.__spriteOffset])

            tiles[objNum].updateState(self.__sheet, 1)
            tiles[self.__blueWeaponSelectButtonsCur].updateState(self.__sheet, -1)
            
            self.__blueWeaponSelectButtonsCur = objNum
            body = tiles[objNum - self.__newBodyOffset].getTileNum()
            
            tiles[objNum - self.__newBodyOffset].update(1, self.__sheet.getSpritesList()[1])
            tiles[objNum - self.__newBodyOffset - self.__newHeadOffset].update(1, self.__sheet.getSpritesList()[1])
            
            return body, 'W'
        return None, None
    
    def leverEvent(self, tiles, objNum):
        """
        Handles lever events.

        Args:
            tiles (List[Tiles]): the list of tiles to update
            objNum (int): the object number for the lever
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
        Gets the index of top objects ending.
        Used in message passing.

        Returns:
            int: the index of top objects ending
        """
        return self.__topObjs
            