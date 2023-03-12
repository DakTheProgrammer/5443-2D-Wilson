import pygame
import math
from PIL import Image

from Dust import Dust

"""
    A class used to represent the projectile shot from tanks
    ...

    Attributes
    ----------
    
    image : pygame.Image
        pygames image of sprite
    rect : pygame.Rect
        rectangle of image
    mask : pygame.mask
        collider of projectile
    angle : float
        angle to shoot projectile from
    origin : tuple
        where to shoot the projectile from
    time : int
        time elapsed (for projectile motion)
    power : int
        power of projectile shot
    weight : int
        weight of projectile
    cannonDust : Dust
        dust from shooting
    trail : list
        trail of the projectile
    alive : bool
        to check if its still active 


    Methods
    -------
    draw(screen, power)
        draws all the items on screen
    getCollision(mask, location, item, screen):
        handles the events sent to the game
    getMask()
        gets the collider of the projectile
    destroy()
        "destroys" the projectile by moving it way away
    calculate_new_xy(old_xy,offset,angle_in_radians)
        used to calculate where to start the shot
    isAlive()
        checks if the ball is still actively flying

    """
class Projectile(pygame.sprite.Sprite):
    def __init__(self, origin, angle):
        """
        Parameters
        ----------
        origin : tuple
            location of projectile
        angle : float
            angle of arm to shoot from
        """
        super().__init__()

        self.image = Image.open('Tanks/Projectile/Projectile.png')
        self.image = self.image.crop(self.image.getbbox())
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_size()[0] / 30, self.image.get_size()[1] / 30))
        
        self.rect = self.image.get_rect()

        self.__mask = pygame.mask.from_surface(self.image)
        
        self.__angle = angle
        #where to shoot ball from
        self.__origin = self.__calculate_new_xy(origin, 35, math.radians(self.__angle))

        self.rect.center = self.__origin

        self.__time = 0
        self.__power = 10
        self.__weight = 40

        self.__cannonDust = Dust(self.__origin, 500,(105,105,105))
        self.__trail = []

        self.__alive = True
        

    def draw(self, screen, power):
        """
        draws the projectile flying

        Parameters
        ----------
        screen : pygame.display
            screen from pygame
        power : int
            power of projectile
        """

        #projectile motions math
        self.rect.centerx = (self.rect.centerx + math.cos(math.radians(self.__angle)) * (self.__power + power) * self.__time)
        self.rect.centery = (self.rect.centery - math.sin(math.radians(self.__angle)) * (self.__power + power) * self.__time) + self.__weight * self.__time**2

        self.__trail.append(Dust(self.rect.center, 1))

        self.__time += 1/50

        self.__cannonDust.draw(screen)
        self.__cannonDust.update()

        for part in self.__trail:
            part.draw(screen)
            part.update()

        screen.blit(self.image, self.rect)

    def getCollision(self, mask, location, item, screen):
        """
        gets collisions of the ball

        Parameters
        ----------
        mask : pygame.mask
            projectile to check
        location : int
            location of mask to check
        item : string
            what we are checking against
        screen : pygame.display
            screen from pygame
        
        """

        #how to check for collisions
        offset = (location[0] - self.rect[0], location[1] - self.rect[1])
        overlaps = self.__mask.overlap(mask, offset)

        if item == 'hill' and overlaps != None:
            return True
        elif item == 'crater' and overlaps != None:
            return True
        elif self.rect.centery > screen.get_height():
            #destroys when its too low
            self.destroy()

        return False
        
    def getMask(self):
        """
        gets collider of the ball

        Parameters
        ----------
        
        """
        return self.__mask
    
    def destroy(self):
        """
        moves ball far off screen and marks it as dead

        Parameters
        ----------
        
        """
        self.__alive = False
        self.rect.center = (5000,5000)

    def __calculate_new_xy(self, old_xy,offset,angle_in_radians):
        """
        gets the locations from the arm where to start the shot

        Parameters
        ----------
        old_xy : tuple
            location of ball
        offset : float
            how far from the origin to shoot the ball
        angle_in_radians : float
            radians of the arm angel
        
        """
        new_x = old_xy[0] + (offset*math.cos(-angle_in_radians))
        new_y = old_xy[1] + (offset*math.sin(-angle_in_radians))
        return new_x, new_y
    
    def isAlive(self):
        """
        checks if the ball is still actively flying

        Parameters
        ----------
        """
        return self.__alive