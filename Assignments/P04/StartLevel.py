import pygame

class StartLevel:
    def __init__(self, sheet):
        self.__redCharSelectButtons = [113,114,115,116]
        self.__redCharSelectButtonsCur = 116
        self.__sheet = sheet

    def buttonEvent(self, objNum, tiles):
        if objNum in self.__redCharSelectButtons:
            tiles[objNum].updateState(self.__sheet, 1)
            tiles[self.__redCharSelectButtonsCur].updateState(self.__sheet, -1)

            self.__redCharSelectButtonsCur = objNum