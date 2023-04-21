import pygame
import math

from Weapon import Weapon


class Player(pygame.sprite.Sprite):

    def __init__(self, default, sheet, spawn):


        self.offset = int(math.sqrt(len(sheet) - 1).real)
        self.__sprites = sheet

        #image -> player body
        #this is the main part of the sprite
        self.image = self.__sprites[default]
        self.rect = self.image.get_rect()
        self.rect.topleft = spawn.rect.topleft

        self.head = self.__sprites[default - self.offset]
        self.headRec = self.head.get_rect()
        self.currentFrame = 0
        self.walking = [] #[self.__sprites[default], self.__sprites[default+1], self.__sprites[default+2], self.__sprites[default+3]]
        self.headMove = []
        self.animationBuffer = 0
        self.animationBufferMax = 2

        for i in range(5):
            self.walking.append(self.__sprites[default + i])
            self.headMove.append(self.__sprites[default - self.offset + i])

        self.moveSpeed = 1
        self.facing = 'R'

        self.weapon = Weapon(340,sheet, self.rect)
        self.__attacking = False
        self.attackBuffer = 0

        #self.__barriers = [2,3,4,33,34,35,166,168,212,232,256,258,259,269,290,291,341,360,389,424,450,451,481,482,483,488]
        self.__barriers = [3,35,167,169,181,213,233,257,258,259,260,291,292,297,310,342,361,390,419,420,425,450,451,452,453,482,483,484,485,489]

        self.__canMove = {
            'Up': True,
            'Down': True,
            'Right': True,
            'Left': True
        }

        super().__init__()

    def draw(self, screen):
        if self.animationBuffer == self.animationBufferMax:
            self.animationBuffer = 0
            if self.currentFrame == len(self.walking) - 1:
                    self.currentFrame = 0
            else:
                self.currentFrame += 1
                self.image = self.walking[self.currentFrame]
                self.head = self.headMove[self.currentFrame]
                if self.facing == 'L':
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.head = pygame.transform.flip(self.head, True, False)
        else:
            self.animationBuffer += 1
        
        self.headRec.topleft = (self.rect.topleft[0], self.rect.topleft[1] - self.rect.height)

        if self.__attacking:
            self.weapon.draw(screen, self.rect, self.facing)
            self.attackBuffer +=1
            if self.attackBuffer > 3:
                self.__attacking = False
                self.attackBuffer = 0

        screen.blit(self.image, self.rect)
        screen.blit(self.head, self.headRec)


    #  -y moves up, +y moves down, -x moves left, +x moves right
    def move(self, x, y):
        if x != 0 or y != 0:
            

            if self.facing == 'R' and x < 0:
                self.facing = 'L'
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.facing == 'L' and x > 0:
                self.facing = 'R'
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect.left += x * self.moveSpeed
            self.rect.top += y * self.moveSpeed

            self.__canMove = {
            'Up': True,
            'Down': True,
            'Right': True,
            'Left': True
        }

    def attack(self):
        self.__attacking = True

    def getAttack(self):
        return self.__attacking

    def getCollision(self, objectRecs, objectsTile):

        collisions = self.rect.collidelistall(objectRecs)
        if collisions == []:
            return False
        else:
            for collision in collisions:
                if objectsTile[collision].getTileNum() in self.__barriers:
                    angle = self.__angle_of_line(self.rect.centerx, self.rect.centery, objectRecs[collision].centerx, objectRecs[collision].centery)
                    
                    #use to test for my bad trig
                    #print(angle)

                    if angle > -45 and angle < 45:
                        self.__canMove['Right'] = False
                    
                    if (angle > 135 and angle <= 180) or (angle > -180 and angle < -135):
                        self.__canMove['Left'] = False
                    
                    if angle < -45 and angle > -135:
                        self.__canMove['Down'] = False

                    if angle > 45 and angle < 135:
                        self.__canMove['Up'] = False
                    

    def getCanMove(self, dir):
        return self.__canMove[dir]
    
    def __angle_of_line(self, x1, y1, x2, y2):
        return math.degrees(math.atan2(-(y2-y1), x2-x1))
