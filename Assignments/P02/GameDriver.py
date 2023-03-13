import pygame
from Tank import Tank
from Ground import Ground
from Hill import Hill
from Projectile import Projectile
from Crater import Crater

"""
    A class used to represent the main driver of the game that processes
    all logic

    ...

    Attributes
    ----------
    
    owner : int
        a marker for what player owns the game currently
    screen : pygame.Display
        a screen object used to determine screen metrics
    background : Tuple
        a RGB color for the background
    clock : pygame.time
        a clock that holds the time since game has been running
    fps : int
        the frame rate of the game
    delta : int
        the amount of time between each frame in ms
    running : bool
        a boolean value that is used to make sure the game continues running
    ground : Ground
        the ground of the game
    hill : Hill
        the hill in the middle of the game  
    PlayerOne : Tank
        the tank for player 1
    PlayerTwo : Tank
        the tank for player 2
    projectile : Projectile
        the object shot out of the tanks
    projectile_power : float
        the power of the projectile shot
    font : pygame.font
        the font for the text on screen
    craters : list
        list contacting all of the craters created
    gameOver : bool
        a boolean value that tells if the game is over
    exit : bool
        a boolean that is used to check if the game needs to restart or end
    powerUpInstruction : pygame.Render
        label for upping power
    powerDownInstruction : pygame.Render
        label for lowering power
    moverRightInstruction : pygame.Render
        label for moving right
    moverLeftInstruction : pygame.Render
        label for moving left
    shootInstruction : pygame.Render
        label for shooting projectile from tanks

    Methods
    -------
    gameLoop()
        loops through the game logic
    draw()
        draws all the items on screen
    handleEvent(event):
        handles the events sent to the game
    handleKeysHeld():
        handles when a key is held down
    handleCollisions():
        does all of the collision events in one section
    handleProjectile():
        does all logic when projectile is shot
    handleGameOverEvents(events):
        works with the events when a game over has occurred
    CheckExit():
        checks if the game needs to end completely
    """
class GameDriver:
    def __init__(self, width = 800, height = 800, name = 'Game', fps = 60, background = (0,0,0)):
        """
        Parameters
        ----------
        width (optional): int
            width of the screen
        height (optional): int
            height of the screen
        name (optional): string
            name displayed on the window
        fps (optional): int
            frame rate of game
        background (optional): tuple
            RGB color code of background of screen
        """
        pygame.init()

        self.__owner = 0

        self.__screen = pygame.display.set_mode((height, width))

        pygame.display.set_caption(name)
        self.__background = background

        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0

        self.__running = False
        self.__ground = Ground(self.__screen)
        self.__hill = Hill(self.__screen, self.__ground.getGroundY())
        

        self.__PlayerOne = Tank(1, True, 0, self.__ground.getGroundY())
        self.__PlayerTwo = Tank(2, False, self.__screen.get_width(), self.__ground.getGroundY())

        self.__projectile = None
        self.__projectile_power = 12.5

        self.__font = pygame.font.Font("Fonts/Lora-Bold.ttf", 35)

        self.__powerUpInstruction = self.__font.render("W: Power up", True, ((0, 0, 0)))
        self.__powerDownInstruction = self.__font.render("S: Power up", True, ((0, 0, 0)))
        self.__moverRightInstruction = self.__font.render("D: Move right", True, ((0, 0, 0)))
        self.__moverLeftInstruction = self.__font.render("A: Move left", True, ((0, 0, 0)))
        self.__shootInstruction = self.__font.render("Click: Shoot", True, ((0, 0, 0)))

        self.__craters = []

        self.__gameOver = False

        self.__exit = True

    def gameLoop(self):
        """
        Parameters
        ----------
        """
        self.__running = True

        while self.__running:
            self.draw()
            
            #when true a tank was hit do game over
            if not self.handleCollisions() and not self.__gameOver:
                self.handleProjectile()
                
                if self.__projectile == None:
                    for events in pygame.event.get():
                        self.handleEvent(events)

                    self.handleKeysHeld()
            else:
                self.__gameOver = True
                
                for events in pygame.event.get():

                    if self.handleGameOverEvents(events) == True:
                        return
            
            
            self.__delta = self.__clock.tick(self.__fps)

    def draw(self):
        """
        draws all the items on screen

        Parameters
        ----------
        """
        self.__screen.fill(self.__background)

        #update labels in draw so they look more accurate
        powerLabel = self.__font.render("Power:" + str(int(self.__projectile_power * 4)), True, ((0, 0, 0)))
        TurnLabel = self.__font.render("Player " + str(self.__owner + 1 ) + " Turn", True, (0,0,0))
        self.__screen.blit(powerLabel, (0,0))
        self.__screen.blit(TurnLabel, (self.__screen.get_width() / 3,0))
        self.__screen.blit(self.__powerUpInstruction, (self.__screen.get_width() * .70, 0))
        self.__screen.blit(self.__powerDownInstruction, (self.__screen.get_width() * .70, self.__screen.get_height() * .045))
        self.__screen.blit(self.__moverRightInstruction, (self.__screen.get_width() * .70,self.__screen.get_height() * .09))
        self.__screen.blit(self.__moverLeftInstruction, (self.__screen.get_width() * .70,self.__screen.get_height() * .135))
        self.__screen.blit(self.__shootInstruction, (self.__screen.get_width() * .70,self.__screen.get_height() * .18))
        
        self.__hill.draw(self.__screen)
        
        for crater in self.__craters:
            crater.draw(self.__screen)

        if self.__projectile != None:
            self.__projectile.draw(self.__screen, self.__projectile_power)

        self.__ground.draw(self.__screen)

        self.__PlayerOne.draw(self.__screen)
        self.__PlayerTwo.draw(self.__screen)

        if self.__gameOver:
            gameOverLabelPart1 = self.__font.render("Game Over Player " + str(self.__owner + 1) + " Wins!", True, ((255, 0, 0)))
            gameOverLabelPart2 = self.__font.render("Press r to Restart.", True, ((255, 0, 0)))
            self.__screen.blit(gameOverLabelPart1, (self.__screen.get_width() * .23,self.__screen.get_height() / 2))
            self.__screen.blit(gameOverLabelPart2, (self.__screen.get_width() * .30,self.__screen.get_height() * .55))

        pygame.display.flip()

    def handleEvent(self, event):
        """
        does all event handling provided by pygame

        Parameters
        ----------
        event: pygame.event
            events given through pygame
        """
        if event.type == pygame.QUIT:
            self.__exit = True
            self.__running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #tank shooting noise
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sounds/Boom.mp3'))
            if self.__owner == 0:
                self.__projectile = Projectile(self.__PlayerOne.GetArmPosition(), self.__PlayerOne.GetArmAngle())
                self.__PlayerOne.DisableArm()
            else:
                self.__projectile = Projectile(self.__PlayerTwo.GetArmPosition(), self.__PlayerTwo.GetArmAngle())
                self.__PlayerTwo.DisableArm()

    def handleKeysHeld(self):
        """
        works with all of the keys held down.
        Must be here or else things move unexpectedly.
        this is pygame style.

        Parameters
        ----------
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.__owner == 0:
                self.__PlayerOne.move('left', self.__delta, self.__screen, self.__hill)
            else:
                self.__PlayerTwo.move('left', self.__delta, self.__screen, self.__hill)
        elif keys[pygame.K_d]:
            if self.__owner == 0:
                self.__PlayerOne.move('right', self.__delta, self.__screen, self.__hill)
            else:
                self.__PlayerTwo.move('right', self.__delta, self.__screen, self.__hill)
        
        if keys[pygame.K_w]:
            if self.__projectile_power < 25:
                self.__projectile_power += .1
        elif keys[pygame.K_s]:
            if self.__projectile_power > 0:
                self.__projectile_power -= .1

    def handleCollisions(self):
        """
        works with all info given about collisions

        Parameters
        ----------
        """
        if self.__projectile != None:
                if self.__owner == 0:
                    #when a projectile hits a tank
                    if self.__PlayerTwo.getCollision(self.__projectile.getMask(), self.__projectile.rect, 'proj')[1]:
                        self.__projectile = None
                        return True
                else:
                    if self.__PlayerOne.getCollision(self.__projectile.getMask(), self.__projectile.rect, 'proj')[1]:
                        self.__projectile = None
                        return True

                #if projectile hits hill
                if self.__projectile.getCollision(self.__hill.getMask(), self.__hill.rect, 'hill', self.__screen):
                    #when there are no craters
                    if self.__craters == []:
                        self.__craters.append(Crater(self.__projectile.rect.center))
                        self.__projectile.destroy()
                    else:
                        i = 0
                        #checks if colliding with crater
                        for crater in self.__craters:
                            if self.__projectile.getCollision(crater.getMask(), crater.rect, 'crater', self.__screen):
                                i += 1
                        
                        #if not hitting any craters
                        if i == 0:
                            self.__craters.append(Crater(self.__projectile.rect.center))
                            self.__projectile.destroy()

                return False

    def handleProjectile(self):
        """
        disables and works with info when projectile is shot

        Parameters
        ----------
        """
        #when there is a projectile and its actively moving
        if self.__projectile != None and not self.__projectile.isAlive():
            #disable shooters arm
            if self.__owner == 0:
                self.__PlayerOne.EnableArm()
            else:
                self.__PlayerTwo.EnableArm()
            
            # 0->1 1->0
            self.__owner = self.__owner ^ 1
            
            self.__PlayerOne.ChangeTurn()
            self.__PlayerTwo.ChangeTurn()
            self.__projectile = None

            #reset projectile power for next player
            self.__projectile_power = 12.5

    def handleGameOverEvents(self, events):
        """
        Parameters
        ----------
        event : pygame.event
            events given by pygame
        """
        if events.type == pygame.QUIT:
            self.__running = False
            self.__exit = True
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_r:
                self.__running = False
                self.__exit = False
                return True
        return False
        
    def CheckExit(self):
        """
        checks if the game needs to completely exit

        Parameters
        ----------
        """
        return self.__exit