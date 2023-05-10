import pygame
import ast
from SpriteSheet import SpriteSheet
from Map import Map
from Player import Player
from StartLevel import StartLevel
from LevelOne import LevelOne
from LevelTwo import LevelTwo
from LevelThree import LevelThree
from GUI import GUI


class GameDriver:
    """
    This class is the main driver for the game. It handles the game loop, 
    drawing, and event handling. It also handles the communication between the two players.

    Attributes
    ----------
    __background : tuple
        The background color of the game window
    __screen : pygame.Surface
        The game window
    __clock : pygame.time.Clock
        The game clock
    __fps : int
        The frames per second
    __delta : int
        The time between frames
    __running : bool
        Whether the game is running or not
    __zoomIn : bool
        Whether the game is zoomed in or not
    __messenger : Messenger 
        The messenger object that handles the communication between the two players
    __Updates : dict
        The dictionary that holds the updates that are sent to the other player
    __partner : str
        The name of the other player
    __newLevelSound : pygame.mixer.Sound
        The sound that plays when the players move to a new level
    __levels : list
        The list of levels
    __levelNum : int
        The current level number
    __spriteSheet : SpriteSheet
        The sprite sheet object
    __map : Map
        The map object
    __level : Level
        The level being played
    __players : list
        The list of players
    __GUI : GUI
        The GUI on the screen
    __owner : int
        The index of the player that is the owner of the game
    
    Methods
    -------
    GameLoop()
        The main game loop
    __draw()
        Draws the game
    __handleEvents()
        Handles the events like key presses
    __checkCollisions()
        Checks for collisions
    __checkNewLevel()
        Checks if the players have moved to a new level
    __setUpdates()
        Sets the updates that are sent to the other player
    __receiveMessage(ch, method, properties, body)
        Receives messages from the other player
    __sendMessage(target, body)
        Sends messages to the other player
    
    """
    def __init__(self, title, messenger ,background = (255,255,255), height = 800, width = 800, fps = 60):
        """The constructor for the GameDriver class that initializes the game window and the game objects
        as well as the messenger object and the messenger callback so that the game can communicate with the other player

        Args:
            title (str): the title of the game window
            messenger (Messenger): the messenger object that handles The communication between the two players
            background (tuple, optional): Defaults to (255,255,255). The background color of the game window
            height (int, optional): Defaults to 800. The height of the game window
            width (int, optional): Defaults to 800. The width of the game window
            fps (int, optional): Defaults to 60. The frames per second
        """
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
        self.__newLevelSound = pygame.mixer.Sound("Assets/sounds/game-pop.wav")
        # self.__walkSound = pygame.mixer.Sound("Assets/sounds/running-in-grass.wav")
        self.__attackSound = pygame.mixer.Sound("Assets/sounds/mixkit-fast-whip-strike-1511.wav")
        
        pygame.display.set_caption(title)
        
        self.__levels = ['./Levels/Start.tmx', './Levels/LevelOne.tmx', './Levels/LevelTwo.tmx', './Levels/LevelThree.tmx']
        self.__levelNum = 0
        
        self.__spriteSheet = SpriteSheet(self.__levels[self.__levelNum])
        self.__map = Map(self.__levels[self.__levelNum], self.__spriteSheet.getSpritesList())
        self.__level = StartLevel(self.__spriteSheet)
        
        self.__players = [Player(41, self.__spriteSheet.getSpritesList(), self.__map.getSpawnTile()[0], self.__level), Player(105, self.__spriteSheet.getSpritesList(), self.__map.getSpawnTile()[1], self.__level)]
        self.__GUI = GUI(self.__spriteSheet.getSpritesList())
        self.__map.setPlayers(self.__players)
        
        messenger.setCallback(self.__receiveMessage)
        
        #sends message to see who's in the game
        self.__sendMessage('broadcast', {'type': 'who'})
        
        #used to determine which player is playing 0 is host 1 is p2
        self.__owner = 0
        
        self.__resets = [False, False]

    def GameLoop(self):
        """
        The main game loop that handles the game loop, drawing, event handling, and communication between the two players

        Parameters
        ----------
        """
        while self.__running:
            self.__draw()

            self.__handleEvents()

            self.__checkCollisions()

            self.__delta = self.__clock.tick(self.__fps)
            
            self.__setUpdates()
            
            self.__sendMessage(self.__partner, self.__Updates)
            
            self.__checkNewLevel()

            self.__checkResetGame()

    def __draw(self):
        """
        The method that draws the game screen as well as the GUI and the zoomed in screen

        Parameters
        ----------
        """
        
        
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
        else:
            self.__GUI.draw(self.__screen, 0, 0)
       
        pygame.display.flip()

    def __handleEvents(self):
        """
        The method that handles the events like key presses

        Parameters
        ----------
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.__players[self.__owner].getAttack():
                    self.__attackSound.set_volume(.07)
                    self.__attackSound.play()
                    self.__players[self.__owner].attack()
                if event.key == pygame.K_o:
                    self.__players[self.__owner].moveSpeed = 0
                if event.key == pygame.K_r:
                    self.__resets[0] = True
                  
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
        # if (x != 0 or y!= 0) and self.__walkSound.get_num_channels() < 1 and self.__players[self.__owner].moveSpeed == 1:
        #     self.__walkSound.set_volume(.1)
        #     self.__walkSound.play()
        # elif x == 0 and y == 0:
        #     self.__walkSound.stop()
            
        self.__players[self.__owner].move(x,y)

        if is_key_pressed[pygame.K_z]:
            self.__zoomIn = False
        else:
            self.__zoomIn = True
        
    def __checkCollisions(self):
        """
        The method that checks for collisions

        Parameters
        ----------
        """
        if self.__players[self.__owner].moveSpeed != 0:
            self.__players[self.__owner].getCollision(self.__map.getObjectRecs(),self.__map.getObjects(), self.__map)
        self.__GUI.update(self.__players[self.__owner].getHealth(),self.__players[self.__owner].getScore())
     
    def __checkNewLevel(self):
        """
        The method that checks if the players have moved to a new level

        Parameters
        ----------
        """
        
        if self.__players[0].moveSpeed == 0 and self.__players[1].moveSpeed == 0 and self.__levelNum != 3:
            self.__newLevelSound.set_volume(.1)
            self.__newLevelSound.play()
            for player in self.__players: player.moveSpeed = 1
            self.__levelNum += 1
            self.__map = Map(self.__levels[self.__levelNum], self.__spriteSheet.getSpritesList())
            
            self.__players[0].rect.topleft = self.__map.getSpawnTile()[0].rect.topleft
            self.__players[1].rect.topleft = self.__map.getSpawnTile()[1].rect.topleft

            self.__map.setPlayers(self.__players)
            
            if self.__levelNum == 1:
                self.__level = LevelOne(self.__spriteSheet, self.__map.getPortalTile()[self.__owner])
            elif self.__levelNum == 2:
                self.__level = LevelTwo(self.__spriteSheet, self.__map.getPortalTile()[self.__owner])
            elif self.__levelNum == 3:
                self.__level = LevelThree(self.__spriteSheet, self.__map.getPortalTile()[self.__owner])
            
            self.__players[self.__owner].setCurrentLevel(self.__level)
            
    def __setUpdates(self):
        """
        The method that sets the updates that are sent to the other player

        Parameters
        ----------
        """
        self.__Updates = {'type': 'updates',
                            'pos': self.__players[self.__owner].rect.topleft,
                            'facing': self.__players[self.__owner].facing,
                            'body': self.__players[self.__owner].defaultSprite,
                            'weapon': self.__players[self.__owner].getWeaponSprite(),
                            'attacking': int(self.__players[self.__owner].getAttack()),
                            'ready': self.__players[self.__owner].moveSpeed,
                            'level': self.__levelNum,
                            'tp': int(self.__players[self.__owner].tp),
                            'reset': int(self.__resets[0])
                            } 
        
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
        """
        This method receives messages from the other player and handles them

        Args:
            ch (Channel): The channel that the message was received on
            method (Method): The method that the message was received on
            properties (Properties): The properties of the message
            body (Binary JSON): The message that was received
        """
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
            if bodyDic['attacking'] == 1: self.__players[self.__owner ^ 1].attack()
            self.__players[self.__owner ^ 1].moveSpeed = bodyDic['ready']
            self.__players[self.__owner ^ 1].tp = bodyDic['tp']

            
            
            if self.__levelNum == bodyDic['level']:
                objects = self.__map.getObjects()
                sprites = self.__spriteSheet.getSpritesList()
                for set in bodyDic['tiles']:
                    objects[set[0]].update(set[1], sprites[set[1]])
                    
            if self.__players[self.__owner].tp and self.__players[self.__owner ^ 1].tp:
                self.__players[self.__owner].teleport()

            self.__resets[1] = bodyDic['reset']
            
                
                
        
    def __sendMessage(self, target, body):
        """
        This method sends messages to the other player

        Args:
            target (str): The person that the message is being sent to
            body (dict): The dictionary that is being sent
        """
        if target != None:
            self.__messenger.send(target, body)

    def __checkResetGame(self):

        if self.__resets[0] and self.__resets[1]:
            self.__players = [Player(41, self.__spriteSheet.getSpritesList(), self.__map.getSpawnTile()[0], self.__level), Player(105, self.__spriteSheet.getSpritesList(), self.__map.getSpawnTile()[1], self.__level)]

            self.__levelNum = 0
            self.__resets = [False, False]

            for player in self.__players: 
                player.moveSpeed = 1
                player.isOver = False

            
            self.__map = Map(self.__levels[self.__levelNum], self.__spriteSheet.getSpritesList())
            
            self.__players[0].rect.topleft = self.__map.getSpawnTile()[0].rect.topleft
            self.__players[1].rect.topleft = self.__map.getSpawnTile()[1].rect.topleft

            self.__map.setPlayers(self.__players)

            self.__level = StartLevel(self.__spriteSheet)

            self.__players[self.__owner].setCurrentLevel(self.__level)