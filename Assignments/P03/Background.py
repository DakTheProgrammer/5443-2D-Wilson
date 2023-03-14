import pygame
from PIL import Image
from BaseSprite import BaseSprite

class Background:
    def __init__(self, images, numFrames, screen, buffer):
        self.__sprites = []
        self.__files = []
        self.__images = []
        self.__frames = numFrames - 1
        self.__frame = 0
        self.__buffer = 0
        self.__bufferMax = buffer

        #used so the file isn't reopened on every crop
        for file in images:
            self.__files.append(Image.open(file))

        for i in range(numFrames):
            self.__images.append([])

            for file in self.__files:                
                #crops to the best size for screen
                img = file.crop(((file.size[0] / numFrames) * i, 0, (file.size[0] / numFrames) * (i + 1), file.size[1]))
                
                img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
                
                self.__images[i].append(BaseSprite(img, screen.get_size()))
            
            self.__sprites.append(pygame.sprite.Group(self.__images[i]))

    def draw(self, screen):
        self.__sprites[self.__frame].draw(screen)

        if self.__buffer == self.__bufferMax:
            self.__buffer = 0
            
            if self.__frame < self.__frames:
                self.__frame += 1
            else:
                self.__frame = 0
            
        self.__buffer += 1
