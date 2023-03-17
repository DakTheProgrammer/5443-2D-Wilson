import pygame
from pygame.math import Vector2
from PIL import Image
from BaseSprite import BaseSprite
from Bullet import Bullet
from copy import deepcopy
import Util

class Ship:
    def __init__(self, loc):
        self.__health = 100
        self.__score = 0
        self.__imageMul = 1.5

        self.__bodyStates = []
        
        self.__bodyStates.append(pygame.image.load(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Full health.png'))
        self.__bodyStates.append(pygame.image.load(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Slight damage.png'))
        self.__bodyStates.append(pygame.image.load(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Damaged.png'))
        self.__bodyStates.append(pygame.image.load(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Very damaged.png'))

        self.__body = BaseSprite(self.__bodyStates[0], Util.scale(self.__bodyStates[0].get_size(), self.__imageMul), mask=True)

        engine = pygame.image.load('Ship/Main Ship/Main Ship - Engines/Main Ship - Engines - Base Engine.png')

        self.__engine = BaseSprite(engine, Util.scale(engine.get_size(), self.__imageMul), mask=True)
        
        self.__idleStates = []
        
        idleEngineImage = Image.open('Ship/Main Ship/Main Ship - Engine Effects/Main Ship - Engines - Base Engine - Idle.png')
        
        self.__idleFrames = 3
        self.__idleCurrentFrame = 0
        
        for i in range(self.__idleFrames):                
            #crops to the best size for screen
            img = idleEngineImage.crop(((idleEngineImage.size[0] / self.__idleFrames) * i, 0, (idleEngineImage.size[0] / self.__idleFrames) * (i + 1), idleEngineImage.size[1]))

            img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

            self.__idleStates.append(img)
            
        self.__accelStates = []
        
        accelEngineImage = Image.open('Ship/Main Ship/Main Ship - Engine Effects/Main Ship - Engines - Base Engine - Powering.png')
        
        self.__accelFrames = 4
        self.__accelCurrentFrame = 0
        
        for i in range(self.__accelFrames):                
            #crops to the best size for screen
            img = accelEngineImage.crop(((accelEngineImage.size[0] / self.__accelFrames) * i, 0, (accelEngineImage.size[0] / self.__accelFrames) * (i + 1), accelEngineImage.size[1]))

            img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

            self.__accelStates.append(img)
            
        self.__engineThrust = BaseSprite(self.__idleStates[0], Util.scale(self.__idleStates[0].get_size(), self.__imageMul), mask=True)
            
        self.__gunStates = []

        gunImage = Image.open('Ship/Main Ship/Main Ship - Weapons/Main Ship - Weapons - Zapper.png')
        #has 6 frames we want
        #has 14 total frames
        self.__gunFrames = 6
        self.__gunCurrentFrame = 0
        
        for i in range(self.__gunFrames):                
            #crops to the best size for screen
            img = gunImage.crop(((gunImage.size[0] / 14) * i, 0, (gunImage.size[0] / 14) * (i + 1), gunImage.size[1]))

            img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

            self.__gunStates.append(img)

        self.__gun = BaseSprite(self.__gunStates[0], Util.scale(self.__gunStates[0].get_size(), self.__imageMul), mask=True)

        self.__ship = pygame.sprite.Group([self.__gun, self.__engineThrust, self.__engine, self.__body])

        self.__ship.update('Location', loc)
        self.__position = loc

        self.__up = Vector2(0,-1)

        self.__velocity = Vector2(0)

        self.__direction = Vector2(self.__up)

        self.__acceleration = 0.1

        self.__maneuverability = 3
        
        self.__bullets = []
        
        self.__gunBuffer = 0
        self.__gunBufferMax = 4
        
        self.__idleBuffer = 0
        self.__idleBufferMax = 4
        
        self.__accelBuffer = 0
        self.__accelBufferMax = 5
        
        self.__shooting = False
        self.__accelerating = False
        
        self.__startTime = pygame.time.get_ticks()

    def draw(self, screen):  
        for bullet in self.__bullets:
            bullet.draw(screen)
        
        if self.__shooting == True:
            if self.__gunBuffer == self.__gunBufferMax:
                self.__gunBuffer = 0
                
                if self.__gunCurrentFrame != self.__gunFrames - 1:        
                    self.__gun.setImage(self.__gunStates[self.__gunCurrentFrame], self.__imageMul)
                    self.__gunCurrentFrame += 1 
                else:
                    self.__shooting = False
                    self.__gunCurrentFrame = 0
                    self.__gun.setImage(self.__gunStates[self.__gunCurrentFrame], self.__imageMul)
                    self.__bullets.append(Bullet(self.__gun.rect.center, deepcopy(self.__direction), self.__direction.angle_to(self.__up)))
            
            self.__gunBuffer += 1
            
        if self.__accelerating == False:
            if self.__idleBuffer == self.__idleBufferMax:
                    self.__idleBuffer = 0
                    if self.__idleCurrentFrame != self.__idleFrames - 1:        
                        self.__engineThrust.setImage(self.__idleStates[self.__idleCurrentFrame], self.__imageMul)
                        self.__idleCurrentFrame += 1 
                    else:
                        self.__idleCurrentFrame = 0
            self.__idleBuffer += 1 
        else:
            if self.__accelBuffer == self.__accelBufferMax:
                    self.__accelBuffer = 0
                    if self.__accelCurrentFrame != self.__accelFrames - 1:        
                        self.__engineThrust.setImage(self.__accelStates[self.__accelCurrentFrame], self.__imageMul)
                        self.__accelCurrentFrame += 1 
                    else:
                        self.__accelCurrentFrame = 0
                
            self.__accelBuffer += 1 
            self.__accelerating = False
            
        self.__ship.update('Move', [self.__velocity, screen])
        self.__ship.update('Rotate', self.__direction.angle_to(self.__up))
            
        self.__ship.draw(screen)
        
        #heal by 10 every 10 seconds
        if pygame.time.get_ticks() - self.__startTime >= 10000:
            if self.__health <= 90 and self.__health > 0:
                self.__health += 10
                self.__onHealthChange()
            self.__startTime = pygame.time.get_ticks()

    def rotate(self, clockwise = True):
        sign = 1 if clockwise else -1
        angle = self.__maneuverability * sign
        self.__direction.rotate_ip(angle)

    def accelerate(self):
        self.__accelerating = True
        self.__velocity += self.__direction * self.__acceleration

    def AsteroidCollision(self, asteroids):
        for asteroid in asteroids:
            sprite = asteroid.getSprite()
            didIt = [False]
            self.__ship.update('Collide', [sprite.getMask(), sprite.rect], didIt)
            if didIt[0] == True:
                self.__health -= 10
                self.__score -= 5
                self.__onHealthChange()
                
                return True, asteroid
            
        return False, None
        
    def getHealth(self):
        return self.__health
    
    def Shoot(self):
        if self.__shooting == False:
            self.__shooting = True
        
        # self.__bullets.append(Bullet(self.__gun.rect.center + Vector2(0,-30), deepcopy(self.__direction), self.__direction.angle_to(self.__up)))
        
        # self.__bullets.append(Bullet(self.__gun.rect.center + Vector2(0,-60), deepcopy(self.__direction), self.__direction.angle_to(self.__up)))
        
    def BulletCollision(self, asteroids):
        for asteroid in asteroids:
            obj = asteroid.getSprite()
            for bullet in self.__bullets:
                if bullet.CheckCollision(obj):
                    self.__bullets.remove(bullet)
                    self.__score += 10
                    return True, asteroid
                
        return False, None
    
    def __onHealthChange(self):
        if self.__health >= 75:
            self.__body.setImage(self.__bodyStates[0], self.__imageMul)
        elif self.__health >= 50:
            self.__body.setImage(self.__bodyStates[1], self.__imageMul)
        elif self.__health >= 25:
            self.__body.setImage(self.__bodyStates[2], self.__imageMul)
        elif self.__health >= 0:
            self.__body.setImage(self.__bodyStates[3], self.__imageMul)
        else:
            #game over?
            ...
            
    def getScore(self):
        return self.__score