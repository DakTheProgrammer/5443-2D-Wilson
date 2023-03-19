import pygame
from Background import Background
from Ship import Ship
from Asteroid import Asteroid
from HealthBar import HealthBar
from Scores import Scores 


class GameDriver:
    def __init__(self, title, backgroundColor = (255,255,255), height = 800, width = 800, fps = 60, multiplayer = None):
        ########################################################
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('Sounds/ambient-dream.mp3')
        pygame.mixer.music.set_volume(.07)
        pygame.mixer.music.play(-1)
        self.__backgroundColor = backgroundColor
        
        self.__screen = pygame.display.set_mode((height,width))
        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0
        self.__running = True
        self.__asteroidCrash = pygame.mixer.Sound('Sounds/explosion.wav')

        pygame.display.set_caption(title)


        self.__messenger = multiplayer
        
        if multiplayer != None:
            self.__messenger.setCallback(self.__receiveMessage)

        #########################################################

        self.__background = Background(
            [
            'Environment/Backgrounds/Condensed/Starry background  - Layer 01 - Void.png',
            'Environment/Backgrounds/Condensed/Starry background  - Layer 02 - Stars.png',
            'Environment/Backgrounds/Condensed/Starry background  - Layer 03 - Stars.png'
            ], 9,self.__screen, 4
        )

        self.__ship = Ship(self.__screen.get_rect().center)
        self.__asteroids = [Asteroid(self.__screen, 3), Asteroid(self.__screen, 3)]
        self.__healthBar = HealthBar(self.__screen)
        self.__scores = Scores()

        self.__sendMessage({'Message': self.__messenger.user + ' has joined the game'})
        
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
        
        for asteroid in self.__asteroids:
            asteroid.draw(self.__screen)
        self.__scores.draw(self.__screen, self.__ship.getScore())
        self.__healthBar.update(self.__ship.getHealth())    
        self.__healthBar.draw(self.__screen)
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
        shipCollision, asteroidHit = self.__ship.AsteroidCollision(self.__asteroids)
       
        if shipCollision:
            self.__newAsteroids(asteroidHit)
            
            
        bulletCollision, asteroidHit = self.__ship.BulletCollision(self.__asteroids)
        
        if bulletCollision:
            self.__newAsteroids(asteroidHit)
            pygame.mixer.Channel(0).set_volume(.3)
            pygame.mixer.Channel(0).play(self.__asteroidCrash)
            
                
    def __newAsteroids(self, asteroid):
        self.__asteroids.remove(asteroid)

        if asteroid.getScale() > 1:
            self.__asteroids.append(Asteroid(self.__screen, asteroid.getScale() - 1, asteroid.getLocation()))
            self.__asteroids.append(Asteroid(self.__screen, asteroid.getScale() - 1, asteroid.getLocation()))
        else:
            #max astroid's is 2^n
            if len(self.__asteroids) < 6:
                self.__asteroids.append(Asteroid(self.__screen, 3))

    def __receiveMessage(self, ch, method, properties, body):
        print(body)
    
    def __sendMessage(self, bodyDic):
        self.__messenger.send("broadcast", bodyDic)