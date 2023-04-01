import pygame
from pygame.math import Vector2
from PIL import Image
from BaseSprite import BaseSprite
from Bullet import Bullet
from copy import deepcopy
import Util

class Ship:
    """
    A class that represents the battle ships in the game
    
    Attributes
    ----------
    __spawnLoc : tuple
        the location the ship spawns at
    __health : int
        the health of the ship
    __score : int
        the score of the ship
    __imageMul : float
        the image multiplier of the ship
    Colors : list
        the list of colors for the ships
    __color : tuple
        the color of the ship
    __bodyStates : list
        the list of body states of the ship
    __body : BaseSprite
        the body of the ship
    __expStates : list
        the list of explosion states
    expImage : PIL Image
        the image of the ship explosion
    __expFrames : int   
        the number of frames in the explosion animation
    __expCurrentFrame : int
        the current frame of the explosion animation
    __expBuffer : int
        the buffer for the explosion animation
    __expBufferMax : int
        the max buffer for the explosion animation
    __explode : BaseSprite
        the explosion sprite
    engine : pygame.image
        the image of the engine
    __idleStates : list
        the list of idle states
    idleEngineImage : PIL Image
        the image of the idle engine
    __idleFrames : int
        the number of frames in the idle engine animation
    __idleCurrentFrame : int
        the current frame of the idle engine animation
    __accelStates : list
        the list of acceleration states
    accelEngineImage : PIL Image
        the image of the acceleration engine
    __accelFrames : int
        the number of frames in the acceleration engine animation
    __accelCurrentFrame : int
        the current frame of the acceleration engine animation
    __engineThrust : BaseSprite
        the engine thrust on the ship
    gunImage : PIL image
        the image of the gun
    __gunState : int
        the state of the gun
    __gunStates : list
        the list of gun states
    __gunImage : Image
        the image of the gun
    __gunFrames : int
        the number of frames in the gun animation
    __gunCurrentFrame : 
        the current frame of the gun animation
     __gun : BaseSprite
        the gun on the ship
    __ship : pygame.sprite.Group
        the group of sprites for the ship
    __position : tuple
        the ships posittion
    __up : Vector2
        the vector for the up direction
    __velocity : Vector2
        the vector for the velocity
    __direction : Vector2
        the vector for the direction of the ship
    __acceleration : float
        the acceleration of the ship
    __maneuverability : float
        the maneuverability of the ship
    __bullets : list
        the list of bullets
    __expBuffer : int
        the buffer for the explosion animation
    __expBufferMax : int
        the max buffer for the explosion animation
    __gunBuffer : int
        the buffer for the gun animation
    __gunBufferMax : int
        the max buffer for the gun animation
    __idleBuffer : int
        the buffer for the idle engine animation
    __idleBufferMax : int
        the max buffer for the idle engine animation
    __accelBuffer : int
        the buffer for the acceleration engine animation
    __accelBufferMax : int
        the max buffer for the acceleration engine animation
    __shooting : bool
        if the ship is shooting
    __accelerating : bool
        if the ship is accelerating
    __exploding : bool
        if the ship is exploding
    __startTime : pygame.time   
        the start time of the game
    __shipDamage : pygame.mixer
        the sound for the ship taking damage
    __fireBullet = pygame.mixer
        the sound for the ship firing bullets
    __shipExplode : pygame.mixer
        the sound for the ship exploding
 
    Methods
    -------
    draw(screen, delta)
        Draws the ship to the screen
    rotate(clockwise = True)
        Rotates the ship sprite
    accelerate()
        Accelerates the ship according to direction and velocity
    AsteroidCollision(asteroids)
        Checks for collisions with asteroids
    BulletCollision(bullets)
        Checks for collisions with other players bullets
    Shoot()
        Shoots a bullet
    Stop()
        sets velocity of ship to 0 to stop the ship
    __onHealthChange()
        Changes the body of the ship based on health
    getHealth()
        Returns the health of the ship
    getScore()
        Returns the score of the ship
    getLocation()
        Returns the location of the ship
    getVelocity()
        Returns the velocity of the ship
    getColor()
        Returns the color of the ship
    getSprite()
        Returns the sprite for the ship
    gotShot()
        Decrements the health and score of the ship
    
    """
    def __init__(self, loc, player, vel = 0):
        """
        Parameters
        ----------
            loc : tuple
                the location the ship spawns
            player : sprite
                the player in the game
            vel : int, optional 
                Defaults to 0
        """
        self.__spawnLoc = loc
        self.__health = 100
        self.__score = 0
        self.__imageMul = 1.5
        Colors = [(251,250,245),(199,206,250),(255,255,186),(186,225,255),(181,234,215),(255,183,178),(226,240,203),(224,187,228),(229,204,255),(236,221,185)]
        self.__bodyStates = []
        self.__color = Colors[player]
        
        self.__bodyStates.append(Image.open(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Full health.png'))
        self.__bodyStates.append(Image.open(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Slight damage.png'))
        self.__bodyStates.append(Image.open(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Damaged.png'))
        self.__bodyStates.append(Image.open(
            'Ship/Main Ship/Main Ship - Bases/Main Ship - Base - Very damaged.png'))
        
        for i in range(len(self.__bodyStates)):
            image = self.__bodyStates[i].convert("RGBA")
            imageData = image.getdata()
            new_image_data = []
            
            for item in imageData:
                # change all white (also shades of whites) pixels to yellow
                if item[0] in list(range(190, 256)):
                    new_image_data.append(self.__color)
                else:
                    new_image_data.append(item)
                    
            # update image data
            image.putdata(new_image_data)
            self.__bodyStates[i] = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

        self.__body = BaseSprite(self.__bodyStates[0], Util.scale(self.__bodyStates[0].get_size(), self.__imageMul), mask=True)
        
        self.__expStates = []
        
        expImage = Image.open('Ship/explode1.png')
        
        self.__expFrames = 4
        self.__expCurrentFrame = 0
        
        for i in range(self.__expFrames):                
            #crops to the best size for screen
            img = expImage.crop(((expImage.size[0] / self.__expFrames) * i, 0, (expImage.size[0] / self.__expFrames) * (i + 1), expImage.size[1]))
            
            img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

            self.__expStates.append(img)
            
        self.__explode = BaseSprite(self.__expStates[0], Util.scale(self.__expStates[0].get_size(), self.__imageMul), mask=False)

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

        self.__velocity = Vector2(vel)

        self.__direction = Vector2(self.__up)

        self.__acceleration = 0.1

        self.__maneuverability = 3
        
        self.__bullets = []
        
        self.__expBuffer = 0
        self.__expBufferMax = 5
        
        self.__gunBuffer = 0
        self.__gunBufferMax = 4
        
        self.__idleBuffer = 0
        self.__idleBufferMax = 4
        
        self.__accelBuffer = 0
        self.__accelBufferMax = 5
        
        self.__shooting = False
        self.__accelerating = False
        self.__exploding = False 
        
        self.__startTime = pygame.time.get_ticks()

        self.__shipDamage = pygame.mixer.Sound('Sounds/static.wav')
        #self.__boostHealth = pygame.mixer.Sound('Sounds/coin.mp3')
        self.__fireBullet = pygame.mixer.Sound('Sounds/laser.wav')
        self.__shipExplode = pygame.mixer.Sound('Sounds/explosion-debris.wav')
    def draw(self, screen, delta):
        """
        Draws the ship to the screen
        
        Parameters
        ----------
            screen : pygame.display
            delta : 
        """
   
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
                    pygame.mixer.Channel(1).set_volume(.07)
                    pygame.mixer.Channel(1).play(self.__fireBullet)
            
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
            
        

        # self.__ship.update('Explode', [self.__position, screen])
        self.__ship.update('Move', [self.__velocity, screen, delta])
        self.__ship.update('Rotate', self.__direction.angle_to(self.__up))
            
        self.__ship.draw(screen)
        
        if self.__exploding == True: 
            if self.__expBuffer == self.__expBufferMax:
                        self.__expBuffer = 0
                        if self.__expCurrentFrame != self.__expFrames - 1:        
                            self.__explode.setImage(self.__expStates[self.__expCurrentFrame], self.__imageMul)
                            self.__expCurrentFrame += 1 
                        else:
                            self.__exploding = False
                            self.__expCurrentFrame = 0
            self.__explode.update('Location', self.__position)
            self.__expBuffer += 1
            self.__explode.draw(screen)
        

        #heal by 10 every 20 seconds
        if pygame.time.get_ticks() - self.__startTime >= 20000:
            if self.__health <= 90 and self.__health > 0:
                self.__health += 10
                #pygame.mixer.Channel(2).set_volume(.08)
                #pygame.mixer.Channel(2).play(self.__boostHealth)
                self.__onHealthChange()
            self.__startTime = pygame.time.get_ticks()

    def rotate(self, clockwise = True):
        """
        Rotates the group of ship sprites
        
        Parameters
        ----------
            clockwise : bool, optional
                Defaults to True.
        """
        sign = 1 if clockwise else -1
        angle = self.__maneuverability * sign
        self.__direction.rotate_ip(angle)

    def accelerate(self):
        """
        Accelerates the ship
        """
        self.__accelerating = True
        self.__velocity += self.__direction * self.__acceleration

    def AsteroidCollision(self, asteroids):
        """
        Checks for collision between the ship and an asteroid
        
        Parameters
        ----------
            asteroids : sprite

        Returns
        --------
            bool : 
                if collision detected

        """
        for asteroid in asteroids:
            sprite = asteroid.getSprite()
            didIt = [False]
            self.__ship.update('Collide', [sprite.getMask(), sprite.rect], didIt)
            if didIt[0] == True:
                pygame.mixer.Channel(3).set_volume(.05)
                pygame.mixer.Channel(3).play(self.__shipDamage)
                self.__health -= 10
                self.__score -= 5
                self.__onHealthChange()
                
                return True, asteroid
            
        return False, None
    
    def BulletCollision(self, asteroids, players):
        """_summary_

        Parameters
        ----------
            asteroids : sprite
            players : sprite

        Returns
        ---------
            bool :
                if bullet collision detected on another ship or asteroid
        """
        for ship in players:
            if ship != self:
                obj = ship.getSprite()
                for bullet in self.__bullets:
                    if bullet.CheckCollision(obj):
                        self.__bullets.remove(bullet)
                        ship.gotShot()
                        self.__score += 100
                        return True, None
        
        for asteroid in asteroids:
            obj = asteroid.getSprite()
            for bullet in self.__bullets:
                if bullet.CheckCollision(obj):
                    self.__bullets.remove(bullet)
                    self.__health += 10
                    self.__onHealthChange()
                    return True, asteroid
                
        return False, None
    
    def Shoot(self):
        """
        Shooting bullets
        """
        if self.__shooting == False:
            self.__shooting = True
        
        # self.__bullets.append(Bullet(self.__gun.rect.center + Vector2(0,-30), deepcopy(self.__direction), self.__direction.angle_to(self.__up)))
        
        # self.__bullets.append(Bullet(self.__gun.rect.center + Vector2(0,-60), deepcopy(self.__direction), self.__direction.angle_to(self.__up)))
    def Stop(self):
        """
        Stops the ship
        """
        self.__velocity = Vector2(0)    
        
    
    def __onHealthChange(self):
        """
        Changes the ship's body image based on health
        """
        if self.__health >= 75:
            self.__body.setImage(self.__bodyStates[0], self.__imageMul)
        elif self.__health >= 50:
            self.__body.setImage(self.__bodyStates[1], self.__imageMul)
        elif self.__health >= 25:
            self.__body.setImage(self.__bodyStates[2], self.__imageMul)
        elif self.__health > 0:
            self.__body.setImage(self.__bodyStates[3], self.__imageMul)
            
        elif self.__health <= 0:
            self.__exploding = True
            pygame.mixer.Channel(4).set_volume(.2)
            pygame.mixer.Channel(4).play(self.__shipExplode)
            self.__position = self.__body.rect.center
            self.__ship.update('Location', self.__spawnLoc)
            self.__health = 100
            self.__score -= 100
            self.__velocity = Vector2(0)
            self.__onHealthChange()
            
    def getHealth(self):
        """
        Gets the Health of the player's ship
        
        Returns
        -------
            health : int 
        """
        return self.__health 
          
    def getScore(self):
        """
        Gets the score of the player's ship
        
        Returns:
            score : int
        """
        return self.__score
    
    def getLocation(self):
        """ 
        Gets the location of the player's ship

        Returns
        -------
            body : BaseSprite : tuple
        """
        return self.__body.rect.center
    
    def getVelocity(self):
        """
        Gets the velocity of the player's ship
        
        Returns
        -------
            velocity : tuple
        """
        return self.__velocity.x, self.__velocity.y
    
    def getColor(self):
        """
        Gets the color of the player's ship

        Returns
        -------
            color : RGB value
        """
        return self.__color
    
    def getSprite(self):
        """
        Gets the sprite of the player's ship
        
        Returns
        -------
           body : sprite
        """
        return self.__body
    
    def gotShot(self):
        """
        Called when the ship is hit by a bullet
        """
        pygame.mixer.Channel(3).set_volume(.1)
        pygame.mixer.Channel(3).play(self.__shipDamage)
        self.__health -= 20
        self.__score -= 10
        self.__onHealthChange()