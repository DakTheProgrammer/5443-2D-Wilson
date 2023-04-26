import pygame
import ast
from SpriteSheet import SpriteSheet
from Map import Map
from Player import Player
from StartLevel import StartLevel

class GameDriver:
    def __init__(self, title, messenger ,background = (255,255,255), height = 800, width = 800, fps = 60):
        pygame.init()

        self.__background = background
        self.__screen = pygame.display.set_mode((width,height))
        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0
        self.__running = True
        self.__zoomIn = True
        self.__messenger = messenger
        
        messenger.setCallback(self.__receiveMessage)
        
        self.__sendMessage('broadcast', {'type': 'who'})
        
        self.__owner = 0
        
        pygame.display.set_caption(title)
        
        startLevelTmx = './Levels/Start.tmx'
        
        self.__spriteSheet = SpriteSheet(startLevelTmx)
        self.__map = Map(startLevelTmx, self.__spriteSheet.getSpritesList())
        self.__level = StartLevel(self.__spriteSheet)

        #40 is p1 default character
        self.__players = [Player(40, self.__spriteSheet.getSpritesList(), self.__map.getSpawnTile()[0], self.__level), Player(104, self.__spriteSheet.getSpritesList(), self.__map.getSpawnTile()[1], self.__level)]
        
    def GameLoop(self):
        while self.__running:
            self.__draw()

            self.__handleEvents()

            self.__checkCollisions()

            self.__delta = self.__clock.tick(self.__fps)

    def __draw(self):
        
        self.__screen.fill(self.__background)
        self.__map.draw(self.__screen)
        for player in self.__players:
            player.draw(self.__screen)

        
        
        if self.__zoomIn: 
            zoom = pygame.transform.scale2x(self.__screen.copy())#pygame.transform.rotozoom(self.__screen.copy(), 0, 2)
            zoomRec = zoom.get_rect()

            zoomRec.center = ((-self.__players[self.__owner].rect.centerx * 2) + (1.5 * self.__screen.get_width()), (-self.__players[self.__owner].rect.centery * 2) + (1.5 * self.__screen.get_height()))

            if self.__players[self.__owner].rect.left < self.__screen.get_width() * .25:
                zoomRec.left = 0
            elif self.__players[self.__owner].rect.right > self.__screen.get_width() * .75:
                zoomRec.right = self.__screen.get_width()
            
            if self.__players[self.__owner].rect.top < self.__screen.get_height() * .25:
                zoomRec.top = 0
            elif self.__players[self.__owner].rect.bottom > self.__screen.get_height() * .75:
                zoomRec.bottom = self.__screen.get_height()
            
            self.__screen.blit(zoom, zoomRec)
        
        pygame.display.flip()

    def __handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.__players[self.__owner].getAttack():
                    self.__players[self.__owner].attack()
                  
        x,y = 0,0  
        is_key_pressed = pygame.key.get_pressed()    
        if (is_key_pressed[pygame.K_d] or is_key_pressed[pygame.K_RIGHT]) and self.__players[self.__owner].getCanMove('Right'):
            x = 1
        elif (is_key_pressed[pygame.K_a] or is_key_pressed[pygame.K_LEFT]) and self.__players[self.__owner].getCanMove('Left'):
            x = -1
        
        if (is_key_pressed[pygame.K_w] or is_key_pressed[pygame.K_UP]) and self.__players[self.__owner].getCanMove('Up'):
            y = -1
        elif (is_key_pressed[pygame.K_s] or is_key_pressed[pygame.K_DOWN]) and self.__players[self.__owner].getCanMove('Down'):
            y = 1

        self.__players[self.__owner].move(x,y)

        if is_key_pressed[pygame.K_z]:
            self.__zoomIn = False
        else:
            self.__zoomIn = True
        
    def __checkCollisions(self):    
        self.__players[self.__owner].getCollision(self.__map.getObjectRecs(),self.__map.getObjects())
     
    def __receiveMessage(self, ch, method, properties, body):
        bodyDic = ast.literal_eval(body.decode('utf-8'))
        
        if bodyDic['type'] == 'who' and bodyDic['from'] != self.__messenger.user:
            self.__sendMessage(bodyDic['from'], {'type': 'owner', 'owner': self.__owner})
        elif bodyDic['type'] == 'owner':
            self.__owner += 1
        
    def __sendMessage(self, target, body):
        self.__messenger.send(target, body)