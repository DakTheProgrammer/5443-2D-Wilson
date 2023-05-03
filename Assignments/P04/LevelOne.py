import pygame

class LevelOne:
    def __init__(self, sheet, portalLoc):
        self.sheet = sheet.getSpritesList()
        self.__portalButtonLeft = 125
        self.__portalButtonRight = 132
        self.__portalLocation = portalLoc.rect.topleft
        self.__leverLeft = 207
        self.__leverRight = 245
        self.__leverLeftCur = 'L'
        self.__leverRightCur = 'L'
        self.__doorLeft = [172,173,136,137]
        self.__doorRight = [190,191,155,154]
        
    
    
        self.__sheet = sheet
        
    def buttonEvent(self, objNum, tiles, bodySprite, weaponSprite):
        print(2)
        if objNum == self.__portalButtonRight:
            tiles[self.__portalButtonRight].update(389, self.sheet[389])
        else:
            tiles[self.__portalButtonLeft].update(389, self.sheet[389])

        return self.__portalLocation, 'P'
        
    def leverEvent(self, tiles, objNum):
        if objNum == self.__leverLeft:
            if self.__leverLeftCur == 'L':
                self.__leverLeftCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                
                for part in self.__doorLeft:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverLeftCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                
                for part in self.__doorLeft:
                    tiles[part].updateState(self.__sheet, -3)
        else:
            if self.__leverRightCur == 'L':
                self.__leverRightCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                
                for part in self.__doorRight:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverRightCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                
                for part in self.__doorRight:
                    tiles[part].updateState(self.__sheet, -3)
                    
  