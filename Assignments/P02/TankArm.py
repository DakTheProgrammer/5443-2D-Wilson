import pygame
from PIL import Image
import math

class TankArm(pygame.sprite.Sprite):
    def __init__(self, playerNum, owned):
        super().__init__()

        self.__owned = owned

        self.__facing = 'W'

        if playerNum == 1:
            self.image = Image.open('Tanks/tank_model_1/tank_model_1_2_w1.png')
            self.__angle = -180
        else:
            self.image = Image.open('Tanks/tank_model_4/tank_model_4_2_w1.png')
            self.__angle = 0
            
        self.image = self.image.crop(self.image.getbbox())
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        #trims the arm to fit the tank
        self.image = pygame.transform.smoothscale(self.image, ((self.image.get_size()[0] + 6.5) / 2, (self.image.get_size()[1] + 6.5 ) / 2))
        self.__rot_image = self.image
        self.rect = self.image.get_rect()
        self.__disabled = False

    def draw(self, screen):        
        self.rotate()

        #shows collider
        #pygame.draw.rect(screen, (255,0,0), self.rect)

        screen.blit(self.__rot_image, self.rect)

    def setLocation(self, x, y):
        self.rect.center = (x, y)

    def rotate(self):
        if self.__owned and not self.__disabled:
            player_rect = self.image.get_rect(center = self.rect.center)

            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - player_rect.centerx, my - player_rect.centery

            #180 bc starts on left side
            self.__angle = math.degrees(math.atan2(-dy, dx)) - 180

            if self.__facing == 'W':
                if self.__angle < -225:
                    self.__angle = 0
                elif self.__angle < -90:
                    self.__angle = -90
            else:
                if self.__angle < -180:
                    self.__angle = -180
                elif self.__angle > -90:
                    self.__angle = -90

            self.__rot_image = pygame.transform.rotate(self.image, self.__angle)
            self.rect = self.__rot_image.get_rect(center = player_rect.center)

    def flip(self, dir):
        self.__rot_image = pygame.transform.flip(self.__rot_image, True, False)
        self.__facing = dir

    def getAngle(self):
        #this is due to starting at angle 180
        return self.__angle + 180
    
    def ChangeOwned(self):
        self.__owned = not self.__owned

    def Disable(self):
        self.__disabled = True

    def Enable(self):
        self.__disabled = False