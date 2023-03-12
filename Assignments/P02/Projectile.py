import pygame
import math
from PIL import Image

from Dust import Dust

class Projectile(pygame.sprite.Sprite):
    def __init__(self, origin, angle):
        super().__init__()

        self.image = Image.open('Tanks/Projectile/Projectile.png')
        self.image = self.image.crop(self.image.getbbox())
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_size()[0] / 30, self.image.get_size()[1] / 30))
        
        self.rect = self.image.get_rect()

        self.__mask = pygame.mask.from_surface(self.image)
        
        self.__angle = angle
        self.__origin = self.__calculate_new_xy(origin, 35, math.radians(self.__angle))

        self.rect.center = self.__origin

        self.__time = 0
        self.__power = 10
        self.__weight = 40

        self.__cannonDust = Dust(self.__origin, 500,(105,105,105))
        self.__trail = []

        self.__alive = True
        

    def draw(self, screen, power):
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
        offset = (location[0] - self.rect[0], location[1] - self.rect[1])
        overlaps = self.__mask.overlap(mask, offset)

        if item == 'hill' and overlaps != None:
            return True
        elif item == 'crater' and overlaps != None:
            return True
        elif self.rect.centery > screen.get_height():
            self.destroy()

        return False
        
    def getMask(self):
        return self.__mask
    
    def destroy(self):
        self.__alive = False
        self.rect.center = (5000,5000)

    def __calculate_new_xy(self, old_xy,offset,angle_in_radians):
        new_x = old_xy[0] + (offset*math.cos(-angle_in_radians))
        new_y = old_xy[1] + (offset*math.sin(-angle_in_radians))
        return new_x, new_y
    
    def isAlive(self):
        return self.__alive