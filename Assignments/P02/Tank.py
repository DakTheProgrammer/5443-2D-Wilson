import pygame
from PIL import Image
from TankArm import TankArm
from Dust import Dust

class Tank(pygame.sprite.Sprite):
    def __init__(self, playerNum, owned, x = 100, y = 100):
        super().__init__()
        
        self.__owned = owned
        self.__playerNum = playerNum

        if self.__playerNum == 1:
            self.image = Image.open('Tanks/tank_model_1/tank_model_1_1_b.png')
        else:
            self.image = Image.open('Tanks/tank_model_4/tank_model_4_1_b.png')
        
        self.image = self.image.crop(self.image.getbbox())
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_size()[0] / 2, self.image.get_size()[1] / 2))

        self.rect = self.image.get_rect()

        self.__mask = pygame.mask.from_surface(self.image)
        
        self.__facing = 'W'

        self.__Arm = TankArm(playerNum, owned)

        #used to make movements smooth since rects only work in whole numbers'
        self.posx = x

        if self.__playerNum == 1:
            self.__flip('E')
        else:
            x = x - self.rect.width

        self._velocity = 0

        self.__setLocation(x, y - self.rect.height)

        self.__isAlive = True
        self.__deathParticles = []
    
    def getCollision(self, mask, location, item):
        offset = (location[0] - self.rect[0], location[1] - self.rect[1])
        overlaps = self.__mask.overlap(mask, offset)

        if item == 'proj' and overlaps != None:
            self.Death()
            return True
        if item == 'hill' and overlaps != None:
            return True

        

    def draw(self, screen):
        if self.__isAlive:
            self.__setArmLocation()
            self.__Arm.draw(screen)

            #shows collider
            #pygame.draw.rect(screen, (0,255,0), self.rect)

            screen.blit(self.image, self.rect)
        else:
            for part in self.__deathParticles:
                part.draw(screen)
                part.update()

            self.__deathParticles.append(Dust((self.rect.centerx, self.rect.bottom), 20, (226,88,34)))


    def move(self, dir, delta, screen, hill):
        if dir == 'left':
            self.__flip('W')
            self.posx -= .1 * delta
        else:
            self.__flip('E')
            self.posx += .1 * delta
        
        if self.posx < 0:
            self.posx = 0
        
        if self.posx > screen.get_width() - self.rect.width or self.getCollision(hill.getMask(), hill.rect, 'hill'):
            self.posx = self.rect.x
            
        self.rect.x = self.posx

    def __setLocation(self, x, y):
        self.posx = x
        self.rect.topleft = (x, y)
        self.__setArmLocation()
    
    def __setArmLocation(self):
        self.__Arm.setLocation(self.rect.centerx, self.rect.centery - .33 * self.rect.size[1])

    def __flip(self, dir):
        if self.__facing != dir:
            #needed to bounce back after hitting hill
            if self.__facing == 'E':
                self.rect.x -= 5
                self.posx = self.rect.x
            else:
                self.rect.x += 5
                self.posx = self.rect.x
            
            self.__facing = dir
            self.image = pygame.transform.flip(self.image, True, False)
            self.__Arm.flip(dir)
    
    def GetArmPosition(self):
        return self.__Arm.rect.center#right when ang = 0 top when ang = 90
    
    def GetArmAngle(self):
        return self.__Arm.getAngle()
    
    def GetFacing(self):
        return self.__facing
    
    def Death(self):
        self.__isAlive = False
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sounds/Fire.mp3'))