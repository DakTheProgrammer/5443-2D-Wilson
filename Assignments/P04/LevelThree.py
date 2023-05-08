import pygame

class LevelThree:
    def __init__(self, sheet, portalLoc):
        self.sheet = sheet.getSpritesList()
        self.__portalButtonTop = 51
        self.__portalButtonBottom = 300
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
            if self.__leverTopCurR == 'L':
                self.__leverTopCurR = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.play()
                for part in self.__doorTopR:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverTopCurR = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.play()
                for part in self.__doorTopR:
                    tiles[part].updateState(self.__sheet, -3)
                    
        elif objNum == self.__leverTopL:
            if self.__leverTopCurL == 'L':
                self.__leverTopCurL = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.play()
                for part in self.__doorTopL:
                    tiles[part].updateState(self.__sheet, 3)
                    
            else:
                self.__leverTopCurL = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.play()
                for part in self.__doorTopL:
                    tiles[part].updateState(self.__sheet, -3)
               
                    
        elif objNum == self.__leverBottomR:
            if self.__leverBottomCurR == 'L':
                self.__leverBottomCurR = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.play()
                for part in self.__doorBottomR:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverBottomCurR = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.play()
                for part in self.__doorBottomR:
                    tiles[part].updateState(self.__sheet, -3)
                    
        elif objNum == self.__leverBottomL:
            if self.__leverBottomCurL == 'L':
                self.__leverBottomCurL = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.play()
                for part in self.__doorBottomL:
                    tiles[part].updateState(self.__sheet, 3)
                    
            else:
                self.__leverBottomCurL = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.play()
                for part in self.__doorBottomL:
                    tiles[part].updateState(self.__sheet, -3)
                
        

    def getTopObjs(self):
        return self.__topObjs