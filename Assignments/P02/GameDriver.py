import pygame
from Tank import Tank
from Ground import Ground
from Hill import Hill
from Projectile import Projectile
from Crater import Crater

class GameDriver:
    def __init__(self, width = 800, height = 800, name = 'Game', fps = 60, background = (0,0,0)):
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

        self.__craters = []

        self.__gameOver = False

        self.__exit = True

    def gameLoop(self):
        self.__running = True

        while self.__running:
            self.__draw()
            
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

    def __draw(self):
        self.__screen.fill(self.__background)

        powerLabel = self.__font.render("Power:" + str(int(self.__projectile_power * 4)), True, ((0, 0, 0)))
        TurnLabel = self.__font.render("Player " + str(self.__owner + 1 ) + " Turn", True, (0,0,0))
        self.__screen.blit(powerLabel, (0,0))
        self.__screen.blit(TurnLabel, (self.__screen.get_width() / 3,0))
        
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
        if event.type == pygame.QUIT:
            self.__exit = True
            self.__running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sounds/Boom.mp3'))
            if self.__owner == 0:
                self.__projectile = Projectile(self.__PlayerOne.GetArmPosition(), self.__PlayerOne.GetArmAngle())
                self.__PlayerOne.DisableArm()
            else:
                self.__projectile = Projectile(self.__PlayerTwo.GetArmPosition(), self.__PlayerTwo.GetArmAngle())
                self.__PlayerTwo.DisableArm()

    def handleKeysHeld(self):
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
        if self.__projectile != None:
                if self.__owner == 0:
                    if self.__PlayerTwo.getCollision(self.__projectile.getMask(), self.__projectile.rect, 'proj')[1]:
                        self.__projectile = None
                        return True
                else:
                    if self.__PlayerOne.getCollision(self.__projectile.getMask(), self.__projectile.rect, 'proj')[1]:
                        self.__projectile = None
                        return True

                #if projectile hits hill
                if self.__projectile.getCollision(self.__hill.getMask(), self.__hill.rect, 'hill', self.__screen):
                    if self.__craters == []:
                        self.__craters.append(Crater(self.__projectile.rect.center))
                        self.__projectile.destroy()
                    else:
                        i = 0
                        for crater in self.__craters:
                            if self.__projectile.getCollision(crater.getMask(), crater.rect, 'crater', self.__screen):
                                i += 1
                        
                        if i == 0:
                            self.__craters.append(Crater(self.__projectile.rect.center))
                            self.__projectile.destroy()

                return False

    def handleProjectile(self):
        if self.__projectile != None and not self.__projectile.isAlive():
            if self.__owner == 0:
                self.__PlayerOne.EnableArm()
            else:
                self.__PlayerTwo.EnableArm()
            
            self.__owner = self.__owner ^ 1
            
            self.__PlayerOne.ChangeTurn()
            self.__PlayerTwo.ChangeTurn()
            self.__projectile = None

            self.__projectile_power = 12.5

    def handleGameOverEvents(self, events):
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
        return self.__exit