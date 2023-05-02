import pygame

class LevelOne:
    def __init__(self, sheet, portalLoc):
        self.sheet = sheet.getSpritesList()
        self.__portalButton = 125
        self.__portalLocation = portalLoc.rect.topleft
        self.__leverTop = 84
        self.__leverBottom = 245
        self.__leverTopCur = 'L'
        self.__leverBottomCur = 'L'
        self.__doorTop = [73,72,55,54]
        self.__doorBottom = [172,173,136,137]
        self.__exitChest = []
        
    
    
        self.__sheet = sheet
        
    def buttonEvent(self, objNum, tiles, bodySprite, weaponSprite):
        
        if objNum == self.__portalButton:
            tiles[self.__portalButton].update(389, self.sheet[389])

            return self.__portalLocation, 'P'
        
    def leverEvent(self, tiles, objNum):
        if objNum == self.__leverTop:
            if self.__leverTopCur == 'L':
                self.__leverTopCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                
                for part in self.__doorTop:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverTopCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                
                for part in self.__doorTop:
                    tiles[part].updateState(self.__sheet, -3)
        else:
            if self.__leverBottomCur == 'L':
                self.__leverBottomCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                
                for part in self.__doorBottom:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverBottomCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                
                for part in self.__doorBottom:
                    tiles[part].updateState(self.__sheet, -3)
                    
  