import pygame

class LevelThree:
    def __init__(self, sheet, portalLoc):
        self.sheet = sheet.getSpritesList()
        self.__portalButtonTop = 51
        self.__portalButtonBottom = 300
        self.__portalLocation = portalLoc.rect.topleft
        self.__leverTopR = 303
        self.__leverTopL = 215
        self.__leverBottomR = 841
        self.__leverBottomL = 753
        self.__leverTopCur = 'L'
        self.__leverBottomCur = 'L'  
        self.__doorTopL = [191,192,172,173]
        self.__doorTopR = [280,281,258,259]
        self.__doorBottomL = [818,819,796,797]
        self.__doorBottomR = [729,730,710,711]
        
        self.__topObjs = 424
    
        self.__sheet = sheet
        
    def buttonEvent(self, objNum, tiles, bodySprite, weaponSprite):
        if objNum == self.__portalButtonBottom:
            tiles[self.__portalButtonBottom].update(389, self.sheet[389])
        else:
            tiles[self.__portalButtonTop].update(389, self.sheet[389])

        return self.__portalLocation, 'P'
        
    def leverEvent(self, tiles, objNum):
        
        if objNum == self.__leverTopR:
            if self.__leverTopCur == 'L':
                self.__leverTopCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                
                for part in self.__doorTopR:
                    tiles[part].updateState(self.__sheet, 3)
                    
        if objNum == self.__leverTopL:
            if self.__leverTopCur == 'L':
                self.__leverTopCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                    
                for part in self.__doorTopL:
                    tiles[part].updateState(self.__sheet, 3)
                    
            else:
                self.__leverTopCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                
                for part in self.__doorTopL:
                    tiles[part].updateState(self.__sheet, -3)
                
                for part in self.__doorTopR:
                    tiles[part].updateState(self.__sheet, -3)
                    
        if objNum == self.__leverBottomR:
            if self.__leverBottomCur == 'L':
                self.__leverBottomCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                
                for part in self.__doorBottomR:
                    tiles[part].updateState(self.__sheet, 3)
                    
            if objNum == self.__leverBottomL:
                if self.__leverBottomCur == 'L':
                    self.__leverBottomCur = 'R'
                    tiles[objNum].updateState(self.__sheet, 1)
                
                    for part in self.__doorBottomL:
                        tiles[part].updateState(self.__sheet, 3)
                        
            else:
                self.__leverBottomCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                
                for part in self.__doorBottomL:
                    tiles[part].updateState(self.__sheet, -3)
                for part in self.__doorBottomR:
                    tiles[part].updateState(self.__sheet, -3)
                    
        

    def getTopObjs(self):
        return self.__topObjs