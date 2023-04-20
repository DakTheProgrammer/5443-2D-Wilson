import pygame
from SpriteSheet import SpriteSheet
from Map import Map
from Player import Player

class GameDriver:
    def __init__(self, title, background = (255,255,255), height = 800, width = 800, fps = 60):
        pygame.init()

        self.__background = background
        self.__screen = pygame.display.set_mode((width,height))
        self.__clock = pygame.time.Clock()
        self.__fps = fps
        self.__delta = 0
        self.__running = True

        pygame.display.set_caption(title)
        
        startLevel = './Levels/Start.tmx'

        self.__spriteSheet = SpriteSheet(startLevel)
        self.__map = Map(startLevel, self.__spriteSheet.getSpritesList())

        #41 is p1 default character
        self.__playerOne = Player(41, self.__spriteSheet.getSpritesList(),self.__map.getSpawnTile()[0] )
        
    def GameLoop(self):
        while self.__running:
            self.__draw()

            self.__handleEvents()

            self.__checkCollisions()

            self.__delta = self.__clock.tick(self.__fps)

    def __draw(self):
        
        self.__screen.fill(self.__background)
        self.__map.draw(self.__screen)
        self.__playerOne.draw(self.__screen)
        
        zoom = pygame.transform.rotozoom(self.__screen.copy(), 0, 2)
        zoomRec = zoom.get_rect()

        zoomRec.center = ((-self.__playerOne.rect.centerx * 2) + (1.5 * self.__screen.get_width()), (-self.__playerOne.rect.centery * 2) + (1.5 * self.__screen.get_height()))

        if self.__playerOne.rect.left < self.__screen.get_width() * .25:
            zoomRec.left = 0
        elif self.__playerOne.rect.right > self.__screen.get_width() * .75:
            zoomRec.right = self.__screen.get_width()
        
        if self.__playerOne.rect.top < self.__screen.get_height() * .25:
            zoomRec.top = 0
        elif self.__playerOne.rect.bottom > self.__screen.get_height() * .75:
            zoomRec.bottom = self.__screen.get_height()
        
        self.__screen.blit(zoom, zoomRec)
        
        pygame.display.flip()

    def __handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.__playerOne.getAttack():
                    self.__playerOne.attack()
                  
        x,y = 0,0  
        is_key_pressed = pygame.key.get_pressed()    
        if (is_key_pressed[pygame.K_d] or is_key_pressed[pygame.K_RIGHT]) and self.__playerOne.getCanMove('Right'):
            x = 1
        elif (is_key_pressed[pygame.K_a] or is_key_pressed[pygame.K_LEFT]) and self.__playerOne.getCanMove('Left'):
            x = -1
        
        if (is_key_pressed[pygame.K_w] or is_key_pressed[pygame.K_UP]) and self.__playerOne.getCanMove('Up'):
            y = -1
        elif (is_key_pressed[pygame.K_s] or is_key_pressed[pygame.K_DOWN]) and self.__playerOne.getCanMove('Down'):
            y = 1
        self.__playerOne.move(x,y)
        
    def __checkCollisions(self):    
        self.__playerOne.getCollision(self.__map.getObjectRecs(),self.__map.getObjects())
        