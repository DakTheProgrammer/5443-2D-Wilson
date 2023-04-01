import pygame
from PIL import Image
from BaseSprite import BaseSprite
import Util
from pygame.math import Vector2

class Bullet():
    """
    a Bullet class to represent the bullets shooting from the ship
    ...
    Attributes
    ----------
    imgMul : float
        multiplier for imgage sizing
    imgBuf : int
        buffer for image looping
    bufferMax : int
        max buffer for image looping
    __numFrames : int
        number of frames in the animation
    __bulletImages : int
        list of images for the animation
    sprite : pygame.sprite
        sprite for the bullet
    __currentFrame : int
        current frame of the animation
    __velocity : float
        velocity of the bullet
    angle : float
        angle of the bullet
        
    Methods
    -------
    draw(screen) : 
        draws the bullet
    __move() :
        moves the bullet
    CheckCollision(sprite) :
        checks if the bullet sprite has collided with an asteroid or ship
    
    """
    def __init__(self, gun, direction, angle):
        """
        Parameters
        -----------
            gun : 
            direction: 
            angle : 
        """
        self.imgMul = .75
        self.imgBuf = 0
        self.bufferMax = 4
        
        image = Image.open("Ship/Main ship weapons/Main ship weapon - Projectile - Zapper.png")
        
        self.__numFrames = 4
        frameSize = (image.size[0]/self.__numFrames, image.size[1])
        
        self.__bulletImages = []
        
        for i in range(self.__numFrames):                
            #crops to the best size for screen
            img = image.crop((frameSize[0] * i, 0, frameSize[0] * (i + 1), frameSize[1]))
            #img.show()

            img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

            self.__bulletImages.append(img)
            
        self.sprite = BaseSprite(self.__bulletImages[0],Util.scale(self.__bulletImages[0].get_size(), self.imgMul),mask = True)
        
        self.__currentFrame = 0
        # *6 so there are 6 intermediate angeles to shoot from per section of 90 degrees
        self.__velocity = direction * 12
        self.sprite.rect.center = gun
        self.angle = angle
        
        
    def draw(self, screen):
        """
        draws the bullet to the screen
        Parameters
        ----------
            screen : pygame.display
        """
        self.sprite.setImage(self.__bulletImages[self.__currentFrame],self.imgMul)
        if self.imgBuf == self.bufferMax:
            self.imgBuf = 0
            
            if self.__currentFrame < self.__numFrames - 1:
                self.__currentFrame += 1
            else:
                self.__currentFrame = 0
                
        self.imgBuf += 1
        
        self.__move()
        
        self.sprite.draw(screen)
        
        
    def __move(self):
        """
        moves the bullets according to the ships movement
        """
        self.sprite.rect.center = (self.sprite.rect.centerx + round(self.__velocity[0]), self.sprite.rect.centery + round(self.__velocity[1]))

        self.sprite.update('Rotate', self.angle)
        
        
    def CheckCollision(self, sprite):
        """
        checks if the bullet collided with an asteroid or ship
        
        Parameters
        ----------
            sprite : from BaseSprite

        Returns
        -------
            didIt : list[bool]
        """
        didIt = [False]
        self.sprite.update('Collide', [sprite.getMask(), sprite.rect], didIt)
        return didIt[0]