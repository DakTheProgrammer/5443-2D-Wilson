import pygame
import ast
from SpriteSheet import SpriteSheet
from Map import Map
from Player import Player
from StartLevel import StartLevel
from LevelOne import LevelOne
from GUI import GUI
from Score import Score 


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
        self.__Updates = {}
        self.__partner = None
       
        
        messenger.setCallback(self.__receiveMessage)
        
        self.__sendMessage('broadcast', {'type': 'who'})
        
        self.__owner = 0
        
        pygame.display.set_caption(title)
        
        self.__levels = ['./Levels/Start.tmx', './Levels/LevelOne.tmx']
        self.__levelNum = 1
        
        self.__spriteSheet = SpriteSheet(self.__levels[self.__levelNum])
        self.__map = Map(self.__levels[self.__levelNum], self.__spriteSheet.getSpritesList())
        self.__level = LevelOne(self.__spriteSheet, self.__map.getPortalTile()[0])#StartLevel(self.__spriteSheet)
        

        #40 is p1 default character
        self.__players = [Player(41, self.__spriteSheet.getSpritesList(), self.__map.getSpawnTile()[0], self.__level), Player(105, self.__spriteSheet.getSpritesList(), self.__map.getSpawnTile()[1], self.__level)]
        self.__GUI = GUI(self.__spriteSheet.getSpritesList())
        self.__map.setPlayers(self.__players)
        
    def GameLoop(self):
        while self.__running:
            self.__draw()

            self.__handleEvents()

            self.__checkCollisions()

            self.__delta = self.__clock.tick(self.__fps)
            
            self.__setUpdates()
            
            self.__sendMessage(self.__partner, self.__Updates)
            
            self.__checkNewLevel()

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
            
            self.__GUI.draw(zoom, abs(zoomRec[0]), abs(zoomRec[1]))
            
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
        self.__players[self.__owner].getCollision(self.__map.getObjectRecs(),self.__map.getObjects(), self.__map)
        self.__GUI.update(self.__players[self.__owner].getHealth(),self.__players[self.__owner].getScore())
     
    def __checkNewLevel(self):
        if self.__levelNum == 0:
            if self.__players[0].moveSpeed == 0 and self.__players[1].moveSpeed == 0:
                self.__levelNum += 1
                self.__map = Map(self.__levels[self.__levelNum], self.__spriteSheet.getSpritesList())
                
                for player in self.__players: player.moveSpeed = 1
                self.__players[0].rect.topleft = self.__map.getSpawnTile()[0].rect.topleft
                self.__players[1].rect.topleft = self.__map.getSpawnTile()[1].rect.topleft

                self.__map.setPlayers(self.__players)
                
     
    def __setUpdates(self):
        self.__Updates = {'type': 'updates',
                            'pos': self.__players[self.__owner].rect.topleft,
                            'facing': self.__players[self.__owner].facing,
                            'body': self.__players[self.__owner].defaultSprite,
                            'weapon': self.__players[self.__owner].getWeaponSprite(),
                            'attacking': int(self.__players[self.__owner].getAttack()),
                            'ready': self.__players[self.__owner].moveSpeed
                            } 

        if self.__levelNum == 0:
            if self.__owner == 0:
                tiles = []
                for i, tile in enumerate(self.__map.getObjects()[0:self.__level.getTopObjs()]):
                    tiles.append((i,tile.getTileNum()))   
            else:
                tiles = []
                for i, tile in enumerate(self.__map.getObjects()[self.__level.getTopObjs() + 1:]):
                    i += self.__level.getTopObjs() + 1
                    tiles.append((i,tile.getTileNum()))

            self.__Updates.update({'tiles': tiles})

            
     
    def __receiveMessage(self, ch, method, properties, body):
        bodyDic = ast.literal_eval(body.decode('utf-8'))
        if bodyDic['type'] == 'who' and bodyDic['from'] != self.__messenger.user:
            self.__partner = bodyDic['from']
            self.__sendMessage(bodyDic['from'], {'type': 'owner', 'owner': self.__messenger.user})
        elif bodyDic['type'] == 'owner':
            self.__partner = bodyDic['owner']
            self.__owner += 1
        elif bodyDic['type'] == 'updates':
            self.__players[self.__owner ^ 1].rect.topleft = bodyDic['pos']
            self.__players[self.__owner ^ 1].facing = bodyDic['facing']
            self.__players[self.__owner ^ 1].setFrames(bodyDic['body'])
            self.__players[self.__owner ^ 1].weapon.newWeapon(bodyDic['weapon'])
            if bodyDic['attacking'] == 1: self.__players[self.__owner ^ 1].setAttack()
            self.__players[self.__owner ^ 1].moveSpeed = bodyDic['ready']

            if self.__levelNum == 0:
                objects = self.__map.getObjects()
                sprites = self.__spriteSheet.getSpritesList()
                for set in bodyDic['tiles']:
                    objects[set[0]].update(set[1], sprites[set[1]])
                    
                
        
    def __sendMessage(self, target, body):
        if target != None:
            self.__messenger.send(target, body)