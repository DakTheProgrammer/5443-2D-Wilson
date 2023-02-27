import pygame
from Tank import Tank
from Ground import Ground
from Hill import Hill
from Projectile import Projectile
from Crater import Crater

class GameDriver:
    def __init__(self, owner, width = 800, height = 800, name = 'Game', fps = 60, background = (0,0,0)):
        pygame.init()

        self.__turn = 1

        self.__owner = owner

        self.__screen = pygame.display.set_mode((height, width))

        pygame.display.set_caption(name)
        self.__background = background

        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0

        self.__running = False
        self.__ground = Ground(self.__screen)
        self.__hill = Hill(self.__screen, self.__ground.getGroundY())
        
        if self.__owner == 1:
            self.__PlayerOne = Tank(1, True, 0, self.__ground.getGroundY())
            self.__PlayerTwo = Tank(2, False, self.__screen.get_width(), self.__ground.getGroundY())
        else:
            self.__PlayerOne = Tank(1, False, 0, self.__ground.getGroundY())
            self.__PlayerTwo = Tank(2, True, self.__screen.get_width(), self.__ground.getGroundY())

        self.__projectile = None
        self.__projectile_power = 12.5

        self.__font = pygame.font.Font("Fonts/Lora-Bold.ttf", 35)
        self.__powerLabel = self.__font.render("Power:" + str(int(self.__projectile_power * 4)), True, ((0, 0, 0)))

        self.__craters = []
        

    def __draw(self):
        self.__screen.fill(self.__background)

        self.__screen.blit(self.__powerLabel, (0,0))
        
        self.__hill.draw(self.__screen)
        
        
        for crater in self.__craters:
            crater.draw(self.__screen)

        if self.__projectile != None:
            self.__projectile.draw(self.__screen, self.__projectile_power)

        self.__ground.draw(self.__screen)

        self.__PlayerOne.draw(self.__screen)
        self.__PlayerTwo.draw(self.__screen)

        pygame.display.flip()

    def gameLoop(self):
        self.__running = True

        while self.__running:
            self.__draw()

            for events in pygame.event.get():
                self.handleEvent(events)
            
            if self.__projectile != None:
                if self.__turn == 1:
                    self.__PlayerTwo.getCollision(self.__projectile.getMask(), self.__projectile.rect, 'proj')
                elif self.__turn == 2:
                    self.__PlayerOne.getCollision(self.__projectile.getMask(), self.__projectile.rect, 'proj')

                #if projectile hits hill
                if self.__projectile.getCollision(self.__hill.getMask(), self.__hill.rect, 'hill'):
                    if self.__craters == []:
                        self.__craters.append(Crater(self.__projectile.rect.center))
                        self.__projectile.destroy()
                    else:
                        i = 0
                        for crater in self.__craters:
                            if self.__projectile.getCollision(crater.getMask(), crater.rect, 'crater'):
                                i += 1
                        
                        if i == 0:
                            self.__craters.append(Crater(self.__projectile.rect.center))
                            self.__projectile.destroy()
                        
                    

            self.handleKeysHeld()
            
            self.__delta = self.__clock.tick(self.__fps)

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.__running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sounds/Boom.mp3'))
            if self.__owner == 1:
                self.__projectile = None
                self.__projectile = Projectile(self.__PlayerOne.GetArmPosition(), self.__PlayerOne.GetArmAngle())
            else:
                self.__projectile = None
                self.__projectile = Projectile(self.__PlayerTwo.GetArmPosition(), self.__PlayerTwo.GetArmAngle())

    def handleKeysHeld(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.__owner == 1:
                self.__PlayerOne.move('left', self.__delta, self.__screen, self.__hill)
            else:
                self.__PlayerTwo.move('left', self.__delta, self.__screen, self.__hill)
        elif keys[pygame.K_d]:
            if self.__owner == 1:
                self.__PlayerOne.move('right', self.__delta, self.__screen, self.__hill)
            else:
                self.__PlayerTwo.move('right', self.__delta, self.__screen, self.__hill)
        
        if keys[pygame.K_w]:
            if self.__projectile_power < 25:
                self.__projectile_power += .1
                self.__powerLabel = self.__font.render("Power:" + str(int(self.__projectile_power * 4)), True, ((0, 0, 0)))
        elif keys[pygame.K_s]:
            if self.__projectile_power > 0:
                self.__projectile_power -= .1
                self.__powerLabel = self.__font.render("Power:" + str(int(self.__projectile_power * 4)), True, ((0, 0, 0)))
        