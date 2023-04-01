import pygame
from PIL import Image
from BaseSprite import BaseSprite

class Background:
    """
    A class to represent the Background of the game screen
    
    Attributes
    ----------
    __sprites : list
        list of sprites to be drawn
    __files : list
        list of files to be opened
    __images : list
        list of images to be cropped
    __frames : int
        number of frames in the animation
    __frame : int    
        current frame of the animation
    __buffer : int
        buffer for image looping
    __bufferMax : int
        max buffer for image looping
    
    Methods
    -------
    draw(screen)
        draws the background to the screen
    
    """
    
    def __init__(self, images, numFrames, screen, buffer):
        """
        Parameters
        ----------
            images : list
            numFrames : int
            screen : pygame.display
            buffer : int

        """
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
        """
        draws the Background to the screen

        Parameters
        ----------
            screen : pygame.display
        """
        self.__sprites[self.__frame].draw(screen)

        if self.__buffer == self.__bufferMax:
            self.__buffer = 0
            
            if self.__frame < self.__frames:
                self.__frame += 1
            else:
                self.__frame = 0
            
        self.__buffer += 1
