import pygame
from cmath import sqrt

class StartLevel:
    def __init__(self, sheet):
        self.__redCharSelectButtons = [117,118,119,120]
        self.__blueCharSelectButtons = [278, 279, 280, 281]
        self.__redWeaponSelectButtons = [114,115,116]
        self.__blueWeaponSelectButtons = [275, 276, 277]
        self.__redCharSelectButtonsCur = 120
        self.__blueCharSelectButtonsCur = 281
        self.__redWeaponSelectButtonsCur = 116
        self.__blueWeaponSelectButtonsCur = 277
        self.__newBodyOffset = 18
        self.__newHeadOffset = 9
        
        self.__spriteOffset = int(sqrt(len(sheet.getSpritesList()) - 1).real)
        
        self.__sheet = sheet

    def buttonEvent(self, objNum, tiles, bodySprite, weaponSprite):
        if objNum in self.__redCharSelectButtons:
            tiles[self.__redCharSelectButtonsCur - self.__newBodyOffset].update(bodySprite, self.__sheet.getSpritesList()[bodySprite])
            tiles[self.__redCharSelectButtonsCur - self.__newBodyOffset - self.__newHeadOffset].update(bodySprite - self.__spriteOffset, self.__sheet.getSpritesList()[bodySprite - self.__spriteOffset])

            
            tiles[objNum].updateState(self.__sheet, 1)
            tiles[self.__redCharSelectButtonsCur].updateState(self.__sheet, -1)

            self.__redCharSelectButtonsCur = objNum

            body = tiles[objNum - self.__newBodyOffset].getTileNum()
            
            tiles[objNum - self.__newBodyOffset].update(1, self.__sheet.getSpritesList()[1])
            tiles[objNum - self.__newBodyOffset - self.__newHeadOffset].update(1, self.__sheet.getSpritesList()[1])
            
            return body, 'B'
        
        elif objNum in self.__blueCharSelectButtons:
            tiles[self.__blueCharSelectButtonsCur - self.__newBodyOffset].update(bodySprite, self.__sheet.getSpritesList()[bodySprite])
            tiles[self.__blueCharSelectButtonsCur - self.__newBodyOffset - self.__newHeadOffset].update(bodySprite - self.__spriteOffset, self.__sheet.getSpritesList()[bodySprite - self.__spriteOffset])

            
            tiles[objNum].updateState(self.__sheet, 1)
            tiles[self.__blueCharSelectButtonsCur].updateState(self.__sheet, -1)

            self.__blueCharSelectButtonsCur = objNum

            body = tiles[objNum - self.__newBodyOffset].getTileNum()
            
            tiles[objNum - self.__newBodyOffset].update(1, self.__sheet.getSpritesList()[1])
            tiles[objNum - self.__newBodyOffset - self.__newHeadOffset].update(1, self.__sheet.getSpritesList()[1])
            
            return body, 'B'
        
        elif objNum in self.__redWeaponSelectButtons:
            tiles[self.__redWeaponSelectButtonsCur - self.__newBodyOffset].update(weaponSprite, self.__sheet.getSpritesList()[weaponSprite])
            tiles[self.__redWeaponSelectButtonsCur - self.__newBodyOffset - self.__newHeadOffset].update(weaponSprite - self.__spriteOffset, self.__sheet.getSpritesList()[weaponSprite - self.__spriteOffset])

            tiles[objNum].updateState(self.__sheet, 1)
            tiles[self.__redWeaponSelectButtonsCur].updateState(self.__sheet, -1)
            
            self.__redWeaponSelectButtonsCur = objNum
            body = tiles[objNum - self.__newBodyOffset].getTileNum()
            
            tiles[objNum - self.__newBodyOffset].update(1, self.__sheet.getSpritesList()[1])
            tiles[objNum - self.__newBodyOffset - self.__newHeadOffset].update(1, self.__sheet.getSpritesList()[1])
            
            return body, 'W'
        
        elif objNum in self.__blueWeaponSelectButtons:
            tiles[self.__blueWeaponSelectButtonsCur - self.__newBodyOffset].update(weaponSprite, self.__sheet.getSpritesList()[weaponSprite])
            tiles[self.__blueWeaponSelectButtonsCur - self.__newBodyOffset - self.__newHeadOffset].update(weaponSprite - self.__spriteOffset, self.__sheet.getSpritesList()[weaponSprite - self.__spriteOffset])

            tiles[objNum].updateState(self.__sheet, 1)
            tiles[self.__blueWeaponSelectButtonsCur].updateState(self.__sheet, -1)
            
            self.__blueWeaponSelectButtonsCur = objNum
            body = tiles[objNum - self.__newBodyOffset].getTileNum()
            
            tiles[objNum - self.__newBodyOffset].update(1, self.__sheet.getSpritesList()[1])
            tiles[objNum - self.__newBodyOffset - self.__newHeadOffset].update(1, self.__sheet.getSpritesList()[1])
            
            return body, 'W'
        return None, None
            