import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, img, rect, index):
        self.image = img
        self.rect = pygame.rect.Rect(rect)
        self.__tileNum = index

        self.__barriers = [3,35,66,67,167,169,181,213,233,257,258,259,260,291,292,297,310,342,361,390,391,425,450,451,452,453,482,483,484,485,489]

        self.__Button = [386,388]
        
        self.__Lever = [390,391]
        
        super().__init__()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
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
        
    def updateState(self, sheet, amount):
        self.__tileNum += amount
        self.image = sheet.getSpritesList()[self.__tileNum]

    def update(self, num, img):
        self.image = img
        self.__tileNum = num