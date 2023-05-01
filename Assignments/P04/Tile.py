import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, img, rect, index):
        self.image = img
        self.rect = pygame.rect.Rect(rect)
        self.__tileNum = index

        self.__barriers = [3,5,6,35,38,66,67,99,163,165,166,167,169,181,198,213,233,257,258,259,260,291,292,293,297,310,323,324,342,357,361,390,391,425,450,451,452,453,482,483,484,485,489,628,659]

        self.__coin = [563,564] 
           
        self.__Button = [386,388]
        
        self.__Lever = [390,391]
        
        self.__goblin = [184,185,186,187,188,189,190,191,664,665,666,667,668,669,670,671,696,697,698,699,700,701,702,703,738,739,740,741,742,743,744,745,746,747,748,749,750,751,752,753,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,785]
        
        self.__exit = 358
        
            
        self.animationBuffer = 0
        self.maxBuffer = 7
        
        super().__init__()
    
    def draw(self, screen):
        #this is needed bc message passing and pygame no like each other :(
        try:
            screen.blit(self.image, self.rect)
        except:
            pass
            
        
    def getTileNum(self):
        return self.__tileNum
    
    def isBarrier(self):
        if self.__tileNum in self.__barriers: 
            return True
        else: 
            return False
        
    def isButton(self):
        if self.__tileNum in self.__Button:
            return True
        else:
            return False
    
    def isLever(self):
        if self.__tileNum in self.__Lever:
            return True
        else:
            return False
        
    def isExit(self):
        if self.__tileNum == self.__exit:
            return True
        else:
            return False

    def isCoin(self):
        if self.__tileNum in self.__coin:
            return True
        else:
            return False
        
    def isGoblin(self):
        if self.__tileNum in self.__goblin:
            return True
        else:
            return False
        
    def getCoinsList(self):
        return self.__coin
        
    def updateState(self, sheet, amount):
        self.__tileNum += amount
        self.image = sheet.getSpritesList()[self.__tileNum]

    def update(self, num, img):
        self.image = img
        self.__tileNum = num