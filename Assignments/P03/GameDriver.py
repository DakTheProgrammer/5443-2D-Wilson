import pygame
import ast
import random
from copy import deepcopy
from Background import Background
from Ship import Ship
from Asteroid import Asteroid
from HealthBar import HealthBar
from Scores import Scores 


class GameDriver:
    def __init__(self, title, backgroundColor = (255,255,255), height = 1200, width = 770, fps = 30, multiplayer = None):
        self.__host = False

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('Sounds/ambient-dream.mp3')
        pygame.mixer.music.set_volume(.06)
        pygame.mixer.music.play(-1)
        self.__backgroundColor = backgroundColor
        
        self.__screen = pygame.display.set_mode((height,width))
        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0
        self.__running = True
        self.__asteroidCrash = pygame.mixer.Sound('Sounds/explosion.wav')

        pygame.display.set_caption(title)

        #always 0 bc player one, spawns at random location inside buffer
        self.__ship = Ship((random.randrange(100, self.__screen.get_width() - 100), random.randrange(100, self.__screen.get_height() - 100)), 0)
        self.__asteroids = []
        self.__healthBar = HealthBar(self.__screen)

        #sends a message that someone new has joined the game
        self.__messenger = multiplayer

        self.__scores = Scores(self.__messenger.user, self.__ship.getColor())
        
        if multiplayer != None:
            self.__messenger.setCallback(self.__receiveMessage)
        
            #sends a message asking for what players are already in the game
            self.__sendMessage(
                {'Type': 'Who'})

            self.__sendMessage(
                {'Type': 'Join',
                'Message': self.__messenger.user + ' has joined the game!',
                'Ship': [self.__ship.getLocation(), self.__ship.getVelocity()]})
            
            self.__playerIds = []

        self.__otherPlayers = []
        self.__allPlayers = [self.__ship]

        self.__background = Background(
            [
            'Environment/Backgrounds/Condensed/Starry background  - Layer 01 - Void.png',
            'Environment/Backgrounds/Condensed/Starry background  - Layer 02 - Stars.png',
            'Environment/Backgrounds/Condensed/Starry background  - Layer 03 - Stars.png'
            ], 9,self.__screen, 4
        )

    def GameLoop(self):
        while self.__running:
            self.__CheckCollisions()
            
            self.__Draw()

            self.__HandleEvents()

            self.__delta = self.__clock.tick(self.__fps) / self.__fps

    def __Draw(self):
        self.__screen.fill(self.__backgroundColor)
        self.__background.draw(self.__screen)
        
        for player in self.__otherPlayers:
            player.draw(self.__screen, self.__delta)
        
        self.__ship.draw(self.__screen, self.__delta)
        
        for asteroid in self.__asteroids:
            asteroid.draw(self.__screen, self.__delta)
        self.__scores.draw(self.__screen)
        self.__healthBar.update(self.__ship.getHealth())    
        self.__healthBar.draw(self.__screen)
        pygame.display.flip()

    def __HandleEvents(self):
        sendMessage = False
        Message = {
            'Type': 'Event',
            'Events' : []
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__ship.Shoot()
                    sendMessage = True
                    Message['Events'].append({'Type': 'Shoot'})
                    #self.__sendMessage({'Type': 'Shoot'})
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.__ship.Stop()
                    sendMessage = True
                    Message['Events'].append({'Type': 'Stop'})
                    
                     
        is_key_pressed = pygame.key.get_pressed()
        
        if is_key_pressed[pygame.K_d] or is_key_pressed[pygame.K_RIGHT]:
            self.__ship.rotate(clockwise=True)
            sendMessage = True
            Message['Events'].append({'Type': 'Rotate',
                                'Clockwise': 1})
            # self.__sendMessage({'Type': 'Rotate',
            #                     'Clockwise': 1})
        elif is_key_pressed[pygame.K_a] or is_key_pressed[pygame.K_LEFT]:
            self.__ship.rotate(clockwise=False)
            sendMessage = True
            Message['Events'].append({'Type': 'Rotate',
                                'Clockwise': 0})
            # self.__sendMessage({'Type': 'Rotate',
            #                     'Clockwise': 0})
        if is_key_pressed[pygame.K_w] or is_key_pressed[pygame.K_UP]:
            self.__ship.accelerate()
            sendMessage = True
            Message['Events'].append({'Type': 'Accelerate'})
            #self.__sendMessage({'Type': 'Accelerate'})
        

        if sendMessage == True:
            self.__sendMessage(Message)
            
    def __CheckCollisions(self):
        temp = []
            
        for players in self.__otherPlayers:
            temp.append(players)
        temp.append(self.__ship)
            
        for ship in temp:
            shipCollision, asteroidHit = ship.AsteroidCollision(self.__asteroids)
    
            if shipCollision:
                self.__newAsteroids(asteroidHit)
                self.__scores.update(self.__messenger.user, self.__ship.getScore())
            
            bulletCollision, asteroidHit = ship.BulletCollision(self.__asteroids, temp)
            
            if bulletCollision:
                if asteroidHit != None:
                    self.__newAsteroids(asteroidHit)
                    pygame.mixer.Channel(0).set_volume(.3)
                    pygame.mixer.Channel(0).play(self.__asteroidCrash)
                if ship in self.__otherPlayers:
                    self.__scores.update(self.__playerIds[self.__otherPlayers.index(ship)], ship.getScore())
                else:
                    self.__scores.update(self.__messenger.user, ship.getScore())
                    
                
                    
    def __newAsteroids(self, asteroid):
        self.__asteroids.remove(asteroid)
        # 
        if asteroid.getScale() > 1:
            self.__asteroids.append(Asteroid(self.__screen, asteroid.getScale() - 1, asteroid.getLocation(), -pygame.math.Vector2(asteroid.getVelocity())))
            self.__asteroids.append(Asteroid(self.__screen, asteroid.getScale() - 1, asteroid.getLocation(), asteroid.getVelocity()))
        else:
            #max astroid's is 2^n
            #need host to send new asteroids
            if self.__host:
                if len(self.__asteroids) < 1:
                    self.__asteroids.append(Asteroid(self.__screen, 3))
                    self.__asteroids.append(Asteroid(self.__screen, 3))
                    
                    toSend = []

                    for roid in self.__asteroids:
                        toSend.append([roid.getSize(), roid.getLocation(), roid.getVelocity()])

                    self.__sendMessage({'Type': 'Asteroids',
                                        'Info': toSend})

    def __receiveMessage(self, ch, method, properties, body):
        #print(body)
        #converts bytes to dictionary
        bodyDic = ast.literal_eval(body.decode('utf-8'))
        #print(bodyDic)

        #if a player joins and they aren't yourself (broadcast also sends to self) and they aren't already in the game
        if bodyDic['Type'] == 'Join' and bodyDic['from'] != self.__messenger.user and bodyDic['from'] not in self.__playerIds:
            print('\n' + str(bodyDic['Message']))
            
            self.__otherPlayers.append(Ship(bodyDic['Ship'][0], len(self.__otherPlayers)+1, bodyDic['Ship'][1]))
            self.__allPlayers.append(Ship(bodyDic['Ship'][0], len(self.__otherPlayers)+1, bodyDic['Ship'][1]))
            

            self.__playerIds.append(bodyDic['from'])
            #print(bodyDic['from'])
            self.__scores.addPlayer(bodyDic['from'], self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].getColor())

        #if someone joins the game and requests what users are already in the game
        elif bodyDic['Type'] == 'Who' and bodyDic['from'] != self.__messenger.user:
            if len(self.__playerIds) == 0 and self.__host == False:
                self.__host = True
                self.__asteroids = [Asteroid(self.__screen, 3), Asteroid(self.__screen, 3)]

            self.__sendMessage({'Type': 'Join',
                                'Message': self.__messenger.user + ' is in the game!',
                                'Ship': [self.__ship.getLocation(), self.__ship.getVelocity()]})
            
            if self.__host:
                toSend = []

                for roid in self.__asteroids:
                    toSend.append([roid.getSize(), roid.getLocation(), roid.getVelocity()])

                self.__sendMessage({'Type': 'Asteroids',
                                    'Info': toSend})
        elif bodyDic['Type'] == 'Event' and bodyDic['from'] != self.__messenger.user and bodyDic['from'] in self.__playerIds:
            for dics in bodyDic['Events']:
                #if player accelerates accelerate the given ship 
                if dics['Type'] == 'Accelerate':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].accelerate()
                if dics['Type'] == 'Rotate':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].rotate(clockwise=bool(dics['Clockwise']))
                if dics['Type'] == 'Shoot':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].Shoot()
                if dics['Type'] == 'Stop':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].Stop()
        elif bodyDic['Type'] == 'Asteroids' and bodyDic['from'] != self.__messenger.user and self.__asteroids == []:
            for info in bodyDic['Info']:
                self.__asteroids.append(Asteroid(self.__screen, info[0], info[1], info[2]))
            
            
    def __sendMessage(self, bodyDic):
        self.__messenger.send("broadcast", bodyDic)