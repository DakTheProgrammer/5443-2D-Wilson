import pygame
import math

from Weapon import Weapon


class Player(pygame.sprite.Sprite):
    """
    The player class that controls the player.

    Attributes
    ----------
    defaultSprite : int
        The default sprite
    offset : int
        The offset
    __sprites : list
        The list of sprites
    __coinSound : pygame.mixer.Sound
        The coin sound
    __portalSound : pygame.mixer.Sound
        The portal sound
    __potionSound : pygame.mixer.Sound  
        The potion sound
    __buttonSound : pygame.mixer.Sound
        The button sound
    image : pygame.Surface
        The image
    rect : pygame.Rect
        The rectangle
    head : pygame.Surface
        The head
    headRec : pygame.Rect   
        The head rectangle
    currentFrame : int
        The current frame
    walking : list
        The list of walking sprites
    headMove : list
        The list of head sprites
    animationBuffer : int
        The animation buffer    
    animationBufferMax : int    
        The maximum animation buffer
    __score : int
        The score
    __playerHealth : int    
        The player health
    __milestone : int
        The milestone
    __goblinCollisionCount : int
        The goblin collision count
    __trapCount : int   
        The trap count
    moveSpeed : int
        The move speed
    facing : str    
        The direction the player is facing
    weapon : Weapon 
        The weapon the player has
    __attacking : bool
        The attacking state
    attackBuffer : int
        The attack buffer
    __canMove : dict
        The dictionary of directions the player can move
    __currentLevel : Level
        The current level

    Methods
    -------
    draw(screen)
        Draws the player
    move(x, y)
        Moves the player
    attack()
        Attacks
    getAttack()
        Returns the attacking state
    setAttack() 
        Sets the attacking state
    getCollision(objectRecs, objectTiles, map)  
        Returns the collision
    getCanMove(dir)
        Returns the direction the player can move
    __angle_of_line(x1, y1, x2, y2)
        Returns the angle of the line
    setFrames(default)
        Sets the animation frames
    getWeaponSprite()
        Returns the weapon sprite
    getScore()
        Returns the score
    getHealth()
        Returns the health
    setCurrentLevel(level)
        Sets the current level
    scoreAddHealth()    
        Adds health to the score
    zeroHealth()
        Sets the health to zero
    """

    def __init__(self, default, sheet, spawn, level):
        """
        Constructor for Player class that initializes the player.
        
        Args:
            default (int): the default sprite
            sheet (list): the list of sprites
            spawn (pygame.Rect): the spawn rectangle
            level (Level): the current level
        """

        self.defaultSprite = default
        self.offset = int(math.sqrt(len(sheet) - 1).real)
        self.__sprites = sheet
        self.__coinSound = pygame.mixer.Sound("Assets/sounds/collectcoin.wav")
        self.__portalSound = pygame.mixer.Sound("Assets/sounds/hybrid-arcade-tone.wav")
        self.__potionSound = pygame.mixer.Sound("Assets/sounds/bubbling.wav")
        self.__buttonSound = pygame.mixer.Sound("Assets/sounds/select-sound.wav")
        self.__gameOver = pygame.mixer.Sound("Assets/sounds/winsquare.wav")
        self.__chestOpen = pygame.mixer.Sound("Assets/sounds/slide.wav")
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
        
        self.tp = False
        self.tpLoc = self.rect.topleft
        
        self.isOver = False

        self.__font = pygame.font.Font('Assets/Font/dungeon.ttf', 32)
        self.__gameOverText = self.__font.render("GAME OVER", False, (235, 66, 52))

        super().__init__()

    def draw(self, screen):
        """
        Draws the player.

        Args:
            screen (pygame.Surface): the screen
        """
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

        if self.isOver:
            screen.blit(self.__gameOverText, (self.rect.centerx - self.__gameOverText.get_rect().centerx, self.rect.top))


    #  -y moves up, +y moves down, -x moves left, +x moves right
    def move(self, x, y):
        """
        moves the player.

        Args:
            x (int): the x coordinate to move   
            y (int): the y coordinate to move
        """
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
        """
        the player attacks.
        """
        self.__attacking = True

    def getAttack(self):
        """
        Returns the attacking state.

        Returns:
            bool: the attacking state
        """
        return self.__attacking

    def getCollision(self, objectRecs, objectTiles, map):
        """
        Returns the collision.

        Args:
            objectRecs (list): the list of object rectangles
            objectTiles (list): the list of object tiles
            map (Map): the map

        Returns:
            bool: the collision
        """
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
                    if self.__chestOpen.get_num_channels() < 1:
                        self.__chestOpen.set_volume(.3)
                        self.__chestOpen.play()
                        self.__chestOpen.fadeout(1000)
                    objectTiles[collision].ExitChestAnimation(self.__sprites)
                    self.moveSpeed = 0
                    self.rect.center = objectTiles[collision].rect.center
                if objectTiles[collision].isTreasureChest():
                    objectTiles[collision].TreasureChestAnimation(self.__sprites)
                    pygame.mixer.music.stop()
                    if self.__gameOver.get_num_channels() < 1 and not self.isOver:
                        self.__gameOver.set_volume(.3)
                        self.__gameOver.play()
                        self.__gameOver.fadeout(30000)

                    if self.__score <= 1000:    
                        self.__score += 100
                    else:
                        self.isOver = True
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
                            self.__buttonSound.set_volume(.1)
                            self.__buttonSound.play()
                        elif type == 'W':
                            self.weapon.newWeapon(sprite)
                            self.__buttonSound.set_volume(.1)
                            self.__buttonSound.play()
                        elif type == 'P':
                            self.tpLoc = sprite
                            self.tp = True
                            
                elif objectTiles[collision].isExit():
                    self.moveSpeed = 0
                    self.rect.center = objectTiles[collision].rect.center
                elif objectTiles[collision].isCoin():
                    objectTiles[collision].update(0,self.__sprites[0])
                    self.__coinSound.set_volume(.08)
                    self.__coinSound.play()
                    self.__score += 5
                    self.scoreAddHealth()
                elif objectTiles[collision].isPotion():
                    objectTiles[collision].update(0,self.__sprites[0])
                    self.__potionSound.play()
                    self.__playerHealth +=10
                elif objectTiles[collision].isTrap():
                    self.__trapCount += 1
                    if self.__trapCount > 40 and self.__playerHealth > 0:
                        self.__playerHealth -= 10
                        self.zeroHealth()
                        self.__trapCount = 0

    def getCanMove(self, dir):
        """
        Returns the direction the player can move.

        Args:
            dir (str): the direction

        Returns:
            bool: the direction the player can move
        """
        return self.__canMove[dir]
    
    def __angle_of_line(self, x1, y1, x2, y2):
        """
        Returns the angle of the line.

        Args:
            x1 (int): the x coordinate of the first point
            y1 (int): the y coordinate of the first point
            x2 (int): the x coordinate of the second point
            y2 (int): the y coordinate of the second point

        Returns:
            float: the angle of the line
        """
        return math.degrees(math.atan2(-(y2-y1), x2-x1))

    def setFrames(self, default):
        """
        Sets the animation frames.

        Args:
            default (int): the default sprite
        """
        self.defaultSprite = default
        self.walking = []
        self.headMove = []
        for i in range(5):
            self.walking.append(self.__sprites[default + i])
            self.headMove.append(self.__sprites[default - self.offset + i])
            
    def getWeaponSprite(self):
        """
        Returns the weapon sprite.

        Returns:
            int: the weapon sprite
        """
        return self.weapon.defaultSprite
    
    def getScore(self):
        """
        Returns the score.

        Returns:
            int: the score
        """
        return self.__score
  
    def getHealth(self):
        """
        Returns the health.

        Returns:
            int: the health
        """
        return self.__playerHealth
    
    def setCurrentLevel(self, level):
        """
        Sets the current level.

        Args:
            level (Level): the current level
        """
        self.__currentLevel = level
    
    def scoreAddHealth(self):
        """
        Adds health to the score.
        """
        if  self.__score >= self.__milestone:
            self.__milestone += 100
            self.__playerHealth += 10
            
    def zeroHealth(self):
        """
        Sets the health to zero.
        """
        if self.__playerHealth <= 0:
            self.__playerHealth = 50
            if self.__score >= 25:
                self.__score -= 25
            else:
                self.__score = 0
                
    def teleport(self):
        self.rect.topleft = self.tpLoc
        self.__portalSound.set_volume(.08)
        self.__portalSound.play()
        self.tp = False