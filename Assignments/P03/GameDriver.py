import pygame
from Background import Background
from Ship import Ship
from Asteroid import Asteroid
from Bullet import Bullet

class GameDriver:
    def __init__(self, title, backgroundColor = (255,255,255), height = 800, width = 800, fps = 60):
        ########################################################
        pygame.init()

        self.__backgroundColor = backgroundColor
        
        self.__screen = pygame.display.set_mode((height,width))
        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0
        self.__running = True

        pygame.display.set_caption(title)

        #########################################################

        self.__background = Background(
            [
            'Environment/Backgrounds/Condensed/Starry background  - Layer 01 - Void.png',
            'Environment/Backgrounds/Condensed/Starry background  - Layer 02 - Stars.png',
            'Environment/Backgrounds/Condensed/Starry background  - Layer 03 - Stars.png'
            ], 9,self.__screen, 4
        )

        self.__ship = Ship(self.__screen.get_rect().center)
        self.__asteroid = Asteroid(self.__screen)


    def GameLoop(self):
        while self.__running:
            self.__CheckCollisions()
            
            self.__Draw()

            self.__HandleEvents()

            self.__delta = self.__clock.tick(self.__fps)

    def __Draw(self):
        self.__screen.fill(self.__backgroundColor)
        self.__background.draw(self.__screen)
        
        self.__ship.draw(self.__screen)
        self.__asteroid.draw(self.__screen)
        pygame.display.flip()

    def __HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__ship.Shoot()
                    
        is_key_pressed = pygame.key.get_pressed()


        if is_key_pressed[pygame.K_d]:
            self.__ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_a]:
            self.__ship.rotate(clockwise=False)
        if is_key_pressed[pygame.K_w]:
            self.__ship.accelerate()
            
    def __CheckCollisions(self):
        if self.__ship.CheckCollision(self.__asteroid.getSprite()):
            print('Asteroid!')
        if self.__ship.BulletCollision(self.__asteroid.getSprite()):
            self.__asteroid = Asteroid(self.__screen)