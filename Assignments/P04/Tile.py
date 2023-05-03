import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, img, rect, index):
        self.image = img
        self.rect = pygame.rect.Rect(rect)
        self.__tileNum = index

        self.__barriers = [3,5,6,35,38,66,67,99,163,165,166,167,169,181,198,213,233,226,257,258,259,260,291,292,293,297,310,323,324,342,356,357,361,390,391,425,450,451,452,453,482,483,484,485,489,628,659]

        self.__coin = [563,564] 
           
        self.__Button = [386,388]
        
        self.__Lever = [390,391]
        
        self.__goblin = [56,57,58,59,60,61,62,63,88,89,90,91,92,93,94,95,120,121,122,123,124,125,126,127,184,185,186,187,188,189,190,191,248,249,250,251,252,253,254,255,312,313,314,315,316,317,318,319,344,345,346,347,348,349,350,351,376,377,378,379,380,381,382,383,408,409,410,411,412,413,414,415,440,441,442,443,444,445,446,447,472,473,474,475,476,477,478,479,504,505,506,507,508,509,510,511,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,578,579,580,580,582,583,584,585,586,587,588,589,590,591,592,593,600,601,602,603,604,605,606,607,632,633,634,635,636,637,638,639,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,664,665,666,667,668,669,670,671,674,675,676,677,678,679,680.681,682,683,684,685,686,687,688,696,697,698,699,700,701,702,703,738,739,740,741,742,743,744,745,746,747,748,749,750,751,752,753,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,785]
        
        self.__exit = 358
        
        self.__trap = [355,356,357]
        
        self.__potion = [467,468,469,470,499,500,501,502]
        
        self.__exitChest = [596,597,598]
        
        self.__treasureChest = [628,629,630]
            
        self.animationBuffer = 0
        self.maxBuffer = 7
        self.maxTrapBuffer = 20
        
        self.chestImages = []
        self.chestCur = 0
        self.chestAnimation = False
        
        super().__init__()
    
    def draw(self, screen):
        #this is needed bc message passing and pygame no like each other :(
        try:
            if self.chestAnimation:
                
                self.image = self.chestImages[self.chestCur]
                if self.chestCur != len(self.chestImages) - 1:
                    self.chestCur += 1
                else: 
                    self.chestAnimation = False
                    self.chestCur = 0
            
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
        
    def isTrap(self):
        if self.__tileNum in self.__trap:
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
        
    def isPotion(self):
        if self.__tileNum in self.__potion:
            return True
        else:
            return False
    
    def isTreasureChest(self):
        if self.__tileNum in self.__treasureChest:
            return True
        else:
            return False
        
    def isExitChest(self):
        if self.__tileNum == self.__exitChest[0]:
            return True
        else:
            return False
        
    def ExitChestAnimation(self, sprites):
        if len(self.chestImages) != 3:
            for i in range(3):
                self.chestImages.append(sprites[self.__exitChest[i]])
            self.chestAnimation = True
        
    def getCoinsList(self):
        return self.__coin
        
    def updateState(self, sheet, amount):
        self.__tileNum += amount
        self.image = sheet.getSpritesList()[self.__tileNum]

    def update(self, num, img):
        self.image = img
        self.__tileNum = num