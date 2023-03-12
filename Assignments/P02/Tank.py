import pygame
from PIL import Image
from TankArm import TankArm
from Dust import Dust

"""
    A class used to represent each players tanks

    ...

    Attributes
    ----------
    
    owned : bool
        checks if the tank is currently owned by the player
    playerNum : playerNum   
        the player number that owns that tank
    image : pygame.Image
        the image of the tank
    rect : pygame.Rect
        the rectangle of the tank image
    mask : pygame.mask
        the collider of the tank
    facing : string
        the direction the tank is facing
    Arm : TankArm
        the arm of the tank
    posx : int
        the position of the tank in the x direction
    velocity : int
        the speed of the tank
    isAlive : bool
        if the tank is alive
    deathParticles : list
        the fire that is played when it is dead

    Methods
    -------
    getCollision(mask, location, item)
        gets all collisions with a given item
    draw(screen):
        draws the tank to the screen
    move(dir, delta, screen, hill):
        moves the tank
    setLocation(x, y):
        sets the location of the tank
    setArmLocation():
        sets the location of the arm
    flip(dir):
        flips the image
    GetArmPosition():
        gets the arms positions
    GetArmAngle():
        gets the current arm angle
    GetFacing():
        gets the direction the tank is facing
    Death():
        kills the tanks
    ChangeTurn():
        changes the turn marker for the tank
    DisableArm():
        makes it so the arm cant move
    EnableArm():
        makes it so the arm can move
    """


class Tank(pygame.sprite.Sprite):
    def __init__(self, playerNum, owned, x=100, y=100):
        """
        Parameters
        ----------
        playerNum : int
            the number of the owner to the tank
        owned : bool
            if the tank is in control first 
        x (optional): int
            the x location
        y (optional): int
            the y location
        """
        super().__init__()

        # makes it so sounds dont play on restart
        pygame.mixer.Channel(1).pause()

        self.__owned = owned
        self.__playerNum = playerNum

        if self.__playerNum == 1:
            self.image = Image.open('Tanks/tank_model_1/tank_model_1_1_b.png')
        else:
            self.image = Image.open('Tanks/tank_model_4/tank_model_4_1_b.png')

        self.image = self.image.crop(self.image.getbbox())
        self.image = pygame.image.fromstring(
            self.image.tobytes(), self.image.size, self.image.mode)
        self.image = pygame.transform.smoothscale(
            self.image, (self.image.get_size()[0] / 2, self.image.get_size()[1] / 2))

        self.rect = self.image.get_rect()

        self.__mask = pygame.mask.from_surface(self.image)

        self.__facing = 'W'

        self.__Arm = TankArm(playerNum, owned)

        # used to make movements smooth since rects only work in whole numbers'
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
        """
        Gets if the item is colliding with the tank and 
        if the tank should die

        Parameters
        ----------
        mask : pygame.mask
            the collider to check
        location : tuple
            the location of the collider to check
        item : string
            the name of the item to check
        """
        offset = (location[0] - self.rect[0], location[1] - self.rect[1])
        overlaps = self.__mask.overlap(mask, offset)

        if item == 'proj' and overlaps != None and not self.__owned:
            self.Death()
            return (True, True)
        if item == 'hill' and overlaps != None:
            return (True, False)

        return (False, False)

    def draw(self, screen):
        """
        draws the tank

        Parameters
        ----------
        screen : pygame.Display
            the pygame screen
        """
        if self.__isAlive:
            self.__setArmLocation()
            self.__Arm.draw(screen)

            # shows collider
            #pygame.draw.rect(screen, (0,255,0), self.rect)

            screen.blit(self.image, self.rect)
        else:
            for part in self.__deathParticles:
                part.draw(screen)
                part.update()

            self.__deathParticles.append(
                Dust((self.rect.centerx, self.rect.bottom), 20, (226, 88, 34)))

    def move(self, dir, delta, screen, hill):
        """
        moves the tank around

        Parameters
        ----------
        dir : pygame.mask
            the collider to check
        delta : tuple
            the location of the collider to check
        screen : string
            the name of the item to check
        hill : Hill
            the hill so tank doesn't collide into it
        """
        if dir == 'left':
            self.__flip('W')
            self.posx -= .1 * delta
        else:
            self.__flip('E')
            self.posx += .1 * delta

        if self.posx < 0:
            self.posx = 0

        if self.posx > screen.get_width() - self.rect.width or self.getCollision(hill.getMask(), hill.rect, 'hill')[0]:
            self.posx = self.rect.x

        self.rect.x = self.posx

    def __setLocation(self, x, y):
        """
        sets tanks locations

        Parameters
        ----------
        x : int
            x location to set
        y : int
            y location to set
        """
        self.posx = x
        self.rect.topleft = (x, y)
        self.__setArmLocation()

    def __setArmLocation(self):
        """
        sets arm locations

        Parameters
        ----------
        """
        self.__Arm.setLocation(
            self.rect.centerx, self.rect.centery - .33 * self.rect.size[1])

    def __flip(self, dir):
        """
        flips the tank when turning

        Parameters
        ----------
        dir : string
            direction facing
        """
        if self.__facing != dir:
            # needed to bounce back after hitting hill
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
        """
        Gets the arms position

        Parameters
        ----------
        """
        return self.__Arm.rect.center  # right when ang = 0 top when ang = 90

    def GetArmAngle(self):
        """
        Gets the arms angle

        Parameters
        ----------
        """
        return self.__Arm.getAngle()

    def GetFacing(self):
        """
        Gets the direction the tank is facing

        Parameters
        ----------
        """
        return self.__facing

    def Death(self):
        """
        destroys the tank

        Parameters
        ----------
        """
        self.__isAlive = False
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sounds/Fire.mp3'))

    def ChangeTurn(self):
        """
        changes if the tank should be active or not

        Parameters
        ----------
        """
        self.__owned = not self.__owned
        self.__Arm.ChangeOwned()

    def DisableArm(self):
        """
        disables the arm

        Parameters
        ----------
        """
        self.__Arm.Disable()

    def EnableArm(self):
        """
        enables arms position

        Parameters
        ----------
        """
        self.__Arm.Enable()
