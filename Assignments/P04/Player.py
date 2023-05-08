import pygame
import math

from Weapon import Weapon


class Player(pygame.sprite.Sprite):

    def __init__(self, default, sheet, spawn, level):

        self.defaultSprite = default
        self.offset = int(math.sqrt(len(sheet) - 1).real)
        self.__sprites = sheet
        self.__coinSound = pygame.mixer.Sound("Assets/sounds/collectcoin-6075.mp3")
        self.__portalSound = pygame.mixer.Sound("Assets/sounds/cartoon-jump-6462.mp3")
        self.__potionSound = pygame.mixer.Sound("Assets/sounds/soap-bubbles-pop-96873.mp3")
        self.__buttonSound = pygame.mixer.Sound("Assets/sounds/select-sound-121244.mp3")
        
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
        self.__score = 0
        self.__playerHealth = 100
        self.__milestone = 100
        self.__goblinCollisionCount = 0
        self.__trapCount = 0
        self.setFrames(default)
        
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
    
    def setAttack(self):
        self.__attacking = True

    def getCollision(self, objectRecs, objectTiles, map):
        if self.__attacking and self.attackBuffer == 1:
            if self.weapon.getCollision(objectRecs, objectTiles, self.__currentLevel, map):
                self.__score += 10
                self.scoreAddHealth()
                #print(self.__score)
        
        playerCollisions = self.rect.collidelistall(objectRecs)
        if playerCollisions == []:
            return False
        else:
            for collision in playerCollisions:
                # print(collision)
                #print(objectTiles[collision].getTileNum())
                if objectTiles[collision].isGoblin():
                    self.__goblinCollisionCount +=1
                    
                    # print("G ",self.__goblinCollisionCount)
                    if self.__goblinCollisionCount > 50 and self.__playerHealth > 0:
                        self.__playerHealth -= 10
                        self.zeroHealth()
                        # print("P ",self.__playerHealth)
                        self.__goblinCollisionCount = 0
                if objectTiles[collision].isExitChest():
                    objectTiles[collision].ExitChestAnimation(self.__sprites)
                    self.moveSpeed = 0
                    self.rect.center = objectTiles[collision].rect.center
                if objectTiles[collision].isTreasureChest():
                    objectTiles[collision].TreasureChestAnimation(self.__sprites)
                    self.__score += 100
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
                    sprite, type = self.__currentLevel.buttonEvent(collision, objectTiles, self.defaultSprite, self.weapon.defaultSprite)
                    
                    if sprite != None:
                        if type == 'B':
                            self.setFrames(sprite)
                            self.__buttonSound.play()
                        elif type == 'W':
                            self.weapon.newWeapon(sprite)
                            self.__buttonSound.play()
                        elif type == 'P':
                            self.rect.topleft = sprite
                            self.__portalSound.play()
                            
                elif objectTiles[collision].isExit():
                    self.moveSpeed = 0
                    self.rect.center = objectTiles[collision].rect.center
                elif objectTiles[collision].isCoin():
                    objectTiles[collision].update(0,self.__sprites[0])
                    self.__coinSound.play()
                    self.__score += 5
                    self.scoreAddHealth()
                elif objectTiles[collision].isPotion():
                    objectTiles[collision].update(0,self.__sprites[0])
                    self.__potionSound.play()
                    self.__playerHealth +=10
                elif objectTiles[collision].isTrap():
                    self.__trapCount += 1
                    if self.__trapCount > 50 and self.__playerHealth > 0:
                        self.__playerHealth -= 10
                        self.zeroHealth()
                        self.__trapCount = 0

    def getCanMove(self, dir):
        return self.__canMove[dir]
    
    def __angle_of_line(self, x1, y1, x2, y2):
        return math.degrees(math.atan2(-(y2-y1), x2-x1))

    def setFrames(self, default):
        self.defaultSprite = default
        self.walking = []
        self.headMove = []
        for i in range(5):
            self.walking.append(self.__sprites[default + i])
            self.headMove.append(self.__sprites[default - self.offset + i])
            
    def getWeaponSprite(self):
        return self.weapon.defaultSprite
    
    def getScore(self):
        return self.__score
  
    def getHealth(self):
        return self.__playerHealth
    
    def setCurrentLevel(self, level):
        self.__currentLevel = level
    
    def scoreAddHealth(self):
        if  self.__score >= self.__milestone:
            self.__milestone += 100
            self.__playerHealth += 10
            
    def zeroHealth(self):
        if self.__playerHealth <= 0:
            self.__playerHealth = 50
            if self.__score >= 25:
                self.__score -= 25
            else:
                self.__score = 0