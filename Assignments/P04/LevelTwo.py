import pygame

class LevelTwo:
    def __init__(self, sheet, portalLoc):
        self.sheet = sheet.getSpritesList()
        self.__portalButtonTop = 65
        self.__portalButtonBottom = 259
        self.__portalLocation = portalLoc.rect.topleft
        self.__leverTop = 104
        self.__leverTopCur = 'L'
        self.__leverBottomCur = 'L'
        self.__doorTop = [87,88,70,69]
        self.__doorBottom = [281,282,264,263]
        
        self.__topObjs = 229
    
        self.__sheet = sheet

    def getTopObjs(self):
        return self.__topObjs