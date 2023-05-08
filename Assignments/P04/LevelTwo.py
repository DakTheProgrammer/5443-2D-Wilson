import pygame

class LevelTwo:
    def __init__(self, sheet, portalLoc):
        self.sheet = sheet.getSpritesList()
        self.__portalButtonTop = 51
        self.__portalButtonBottom = 300
        self.__portalLocation = portalLoc.rect.topleft
        self.__leverTop = 145
        self.__leverTopCur = 'L'
        self.__leverBottomCur = 'L'  
        self.__doorTop = [131,132,118,119]
        self.__doorBottom = [380,381,367,368]
        self.__doorOpen = pygame.mixer.Sound("Assets/sounds/open-doors.mp3")
        self.__doorClose = pygame.mixer.Sound("Assets/sounds/door-close.mp3")
        self.__topObjs = 229
    
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
                self.__doorOpen.play()
                for part in self.__doorTop:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverTopCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.play()
                for part in self.__doorTop:
                    tiles[part].updateState(self.__sheet, -3)
        else:
            if self.__leverBottomCur == 'L':
                self.__leverBottomCur = 'R'
                tiles[objNum].updateState(self.__sheet, 1)
                self.__doorOpen.play()
                for part in self.__doorBottom:
                    tiles[part].updateState(self.__sheet, 3)
            else:
                self.__leverBottomCur = 'L'
                tiles[objNum].updateState(self.__sheet, -1)
                self.__doorClose.play()
                for part in self.__doorBottom:
                    tiles[part].updateState(self.__sheet, -3)

    def getTopObjs(self):
        return self.__topObjs