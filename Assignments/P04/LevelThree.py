import pygame

class LevelThree:
    def __init__(self, sheet, portalLoc):
        self.sheet = sheet.getSpritesList()
        self.__portalButtonTop = 51
        self.__portalButtonBottom = 300
        self.__portalLocation = portalLoc.rect.topleft
        self.__leverTop = 303
        self.__leverTopCur = 'L'
        self.__leverBottomCur = 'L'  
        self.__doorTop = [280,281,258,259]
        self.__doorBottom = [809,810,831,832]
        
        self.__topObjs = 450
    
        self.__sheet = sheet
        
    def buttonEvent(self, objNum, tiles, bodySprite, weaponSprite):
        if objNum == self.__portalButtonBottom:
            tiles[self.__portalButtonBottom].update(389, self.sheet[389])
        else:
            tiles[self.__portalButtonTop].update(389, self.sheet[389])

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

    def getTopObjs(self):
        return self.__topObjs