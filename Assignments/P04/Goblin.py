import pygame
import math

class Goblin:
    def __init__(self, tiles, players, sheet):
        """
        This class represents a goblin. It takes in a list of tiles that it will occupy, 
        a list of players that it will attack, and a sprite sheet. 

        Attributes
        ----------
        tiles : list
            A list of tiles that the goblin will occupy
        players : list
            A list of players that the goblin will attack
        sheet : pygame.Surface
            A sprite sheet that the goblin will use to animate itself
        rect : pygame.Rect
            A rectangle that represents the goblin's position and size
        goblinHealth : int  
            The goblin's health
        moveSpeed : int 
            The goblin's movement speed
        moveDelay : int
            The goblin's movement delay
        maxMoveDelay : int 
            The goblin's maximum movement delay
        __canMove : dict
            A dictionary that represents the goblin's ability to move in a direction
        defaults : list
            A list of the goblin's default tiles
        animationNum : int
            The goblin's current animation number
        maxAnimation : int
            The goblin's maximum animation number
        alive : bool
            A boolean that represents whether or not the goblin is alive
        closestPlayer : Player
            The closest player to the goblin
        __goblinDeathSound : pygame.mixer.Sound
            A sound that plays when the goblin dies
        
        Methods
        -------
        move()
            Moves the goblin
        getCollisions(objectRecs, objectTiles)
            Gets the goblin's collisions
        hit(sheet)
            Hits the goblin
        __angle_of_line(x1, y1, x2, y2)
            Gets the angle of a line
        """

        self.sheet = sheet
        self.tiles = tiles
        self.__goblinDeathSound = pygame.mixer.Sound("Assets/sounds/pixel-death.wav")
        if len(self.tiles) == 1:
            self.rect = pygame.rect.Rect(self.tiles[0].rect.topleft, (16, 16))
            self.goblinHealth = 1
        elif len(self.tiles) == 2:
            self.rect = pygame.rect.Rect(self.tiles[0].rect.topleft, (16, 32))
            self.goblinHealth = 2
        else:
            self.rect = pygame.rect.Rect(self.tiles[0].rect.topleft, (32, 32))
            self.goblinHealth = 4
        self.tiles.reverse()

        dist = 10000

        self.closestPlayer = None

        for player in players:
            if math.dist(tiles[0].rect.topleft, player.rect.topleft) < dist:
                dist = math.dist(tiles[0].rect.topleft, player.rect.topleft)
                self.closestPlayer = player
                
        self.moveSpeed = 1
        self.moveDelay = 0
        self.maxMoveDelay = 3
        
        self.__canMove = {
            'Up': True,
            'Down': True,
            'Right': True,
            'Left': True
        }
        
        self.defaults = []
        for tile in self.tiles:
            self.defaults.append(tile.getTileNum())
            
        self.animationNum = 0
        self.maxAnimation = 6
        self.alive = True

    def move(self):
        """
        Moves the goblin and animates it
        """
        if self.alive and self.tiles[0].getTileNum() == 0:
            self.alive = False

        if self.alive:
            if self.moveDelay == self.maxMoveDelay:
                
                if self.animationNum != self.maxAnimation:
                    for tile in self.tiles:
                        if len(self.tiles) < 3:
                            tile.update(tile.getTileNum() + 1, self.sheet[tile.getTileNum() + 1])
                        else:
                            tile.update(tile.getTileNum() + 2, self.sheet[tile.getTileNum() + 2])
                    self.animationNum += 1
                else:
                    self.animationNum = 0
                    for i, tile in enumerate(self.tiles):
                        tile.update(self.defaults[i], self.sheet[self.defaults[i]])

                
                self.moveDelay = 0
                
                x,y = 0,0
                
                for i,tile in enumerate(self.tiles):
                    if i == 0:
                        if tile.rect[0] != self.closestPlayer.rect[0]:
                            if tile.rect[0] < self.closestPlayer.rect[0] and self.__canMove['Right']:
                                tile.rect[0] += self.moveSpeed
                                x = self.moveSpeed
                            elif self.__canMove['Left']:
                                tile.rect[0] -= self.moveSpeed
                                x = -self.moveSpeed
                        
                        if tile.rect[1] != self.closestPlayer.rect[1]:
                            if tile.rect[1] < self.closestPlayer.rect[1] and self.__canMove['Down']:
                                tile.rect[1] += self.moveSpeed
                                y = self.moveSpeed
                            elif self.__canMove['Up']:
                                tile.rect[1] -= self.moveSpeed
                                y = -self.moveSpeed
                    else:
                        tile.rect[0] += x
                        tile.rect[1] += y
                        
                self.rect[0] += x
                self.rect[1] += y
            else:
                self.moveDelay += 1
                
            self.__canMove = {
                    'Up': True,
                    'Down': True,
                    'Right': True,
                    'Left': True
                }
        

    def getCollisions(self, objectRecs, objectTiles):
        """
        Gets the goblin's collisions

        Args:
            objectRecs (List[Recs]): a list of rectangles that the goblin can collide with
            objectTiles (List[Tiles]): a list of tiles that the goblin can collide with

        Returns:
            Bool: whether or not the goblin collided with something
        """
        goblinCollisions = self.rect.collidelistall(objectRecs)
        if goblinCollisions == []:
            return False
        else:
            for collision in goblinCollisions:
                if objectTiles[collision].isBarrier():
                    
                    
                    angle = self.__angle_of_line(self.rect.centerx, self.rect.centery, objectRecs[collision].centerx, objectRecs[collision].centery)
                        
                        #use to test for my bad trig
                        #print(angle)

                    if angle > -45 and angle < 45:
                        self.__canMove['Right'] = False
                    
                    if (angle > 135 and angle <= 180) or (angle > -180 and angle < -135):
                        self.__canMove['Left'] = False
                    
                    if angle < -45 and angle > -135:
                        self.__canMove['Down'] = False

                    if angle > 45 and angle < 135:
                        self.__canMove['Up'] = False
                        
    def hit(self, sheet):
        """
        a method that is called when the goblin is hit

        Args:
            sheet (SpriteSheet): the sprite sheet that the goblin uses
        """
        self.goblinHealth -= 1
        if self.goblinHealth == 0:
            self.__goblinDeathSound.set_volume(.08)
            self.__goblinDeathSound.play()
            for tile in self.tiles:
                tile.update(0, sheet[0])

                        
    def __angle_of_line(self, x1, y1, x2, y2):
        """
        a method that gets the angle of a line

        Args:
            x1 (int): first x point on the line
            y1 (int): first y point on the line
            x2 (int): second x point on the line
            y2 (int): second y point on the line

        Returns:
            float: the angle of a line
        """
        return math.degrees(math.atan2(-(y2-y1), x2-x1))
    
    
