import pygame
from PIL import Image
from BaseSprite import BaseSprite
import Util
from pygame.math import Vector2

class Bullet():
    def __init__(self, gun, direction, angle):
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
        self.__velocity = direction * 6
        self.sprite.rect.center = gun
        self.angle = angle
        
       
        
    def draw(self, screen):
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
        self.sprite.rect.center = (self.sprite.rect.centerx + round(self.__velocity[0]), self.sprite.rect.centery + round(self.__velocity[1]))

        self.sprite.update('Rotate', self.angle)
        
    def CheckCollision(self, sprite):
        didIt = [False]
        self.sprite.update('Collide', [sprite.getMask(), sprite.rect], didIt)
        return didIt[0]