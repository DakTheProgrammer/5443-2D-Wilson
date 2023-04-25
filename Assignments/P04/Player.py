import pygame
import math

from Weapon import Weapon


class Player(pygame.sprite.Sprite):

    def __init__(self, default, sheet, spawn, level):

        self.defaultSprite = default
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

        self.__setFrames(default)

        self.moveSpeed = 1
        self.facing = 'R'

        self.weapon = Weapon(340, sheet, self.rect)
        self.__attacking = False
        self.attackBuffer = 0

        self.__canMove = {
            'Up': True,
            'Down': True,
            'Right': True,
            'Left': True
        }

        self.__currentLevel = level

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

    def getCollision(self, objectRecs, objectTiles):
        if self.__attacking and self.attackBuffer == 1:
            self.weapon.getCollision(objectRecs, objectTiles, self.__currentLevel)
        
        playerCollisions = self.rect.collidelistall(objectRecs)
        if playerCollisions == []:
            return False
        else:
            for collision in playerCollisions:
                
                if objectTiles[collision].isBarrier():
                    
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
                elif objectTiles[collision].isButton():
                    #print(collision)
                    sprite, type = self.__currentLevel.buttonEvent(collision, objectTiles, self.defaultSprite, self.weapon.defaultSprite)
                    if sprite != None:
                        if type == 'B':
                            self.__setFrames(sprite)
                        elif type == 'W':
                            self.weapon.newWeapon(sprite)
                    

    def getCanMove(self, dir):
        return self.__canMove[dir]
    
    def __angle_of_line(self, x1, y1, x2, y2):
        return math.degrees(math.atan2(-(y2-y1), x2-x1))

    def __setFrames(self, default):
        self.defaultSprite = default
        self.walking = []
        self.headMove = []
        for i in range(5):
            self.walking.append(self.__sprites[default + i])
            self.headMove.append(self.__sprites[default - self.offset + i])