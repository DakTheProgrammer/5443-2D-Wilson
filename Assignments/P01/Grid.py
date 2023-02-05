import pygame

class Grid:
    """
    A class used to represent the overlay grid that actually holds
    the tetris game

    ...

    Attributes
    ----------
    screen : pygame.Display
        a screen object used to determine screen metrics
    slots : list
        a list containing the grid structure 2D in 1D format
    slots_rows : int
        number of rows in the grid
    slots_cols : int
        the number columns in the grid
    slots_size : int
        the size of each grid slot
    outline : pygame.Rect
        the outline borders of the grid
    origin : pygame.Rect
        the position where each shape begins

    Methods
    -------
    draw()
        draws the grid
    checkClear(placed)
        Checks the lines to see if they need to be cleared
    getOrigin():
        returns the origin location
    getSlotSize():
        returns the size of each grid unit
    getOutline():
        returns the outline shape
    """

    def __init__(self, screen):
        """
        Parameters
        ----------
        screen : pygame.Display
            The screen used for the game
        """

        self.__screen = screen
        #each grid spot
        self.__slots = []
        self.__slots_rows = 20
        self.__slots_cols = 10
        
        #gets the size the squares can fit on the full screen
        #only need size since squares
        self.__slot_size = screen.get_width() / self.__slots_rows
        
        #outline for the grid
        self.__outline = pygame.Rect(0, 0, self.__slot_size * self.__slots_cols, screen.get_height())

        #creates the rectangles in the grid
        for r in range(self.__slots_rows):
            for c in range(self.__slots_cols):
                self.__slots.append(pygame.Rect(c * self.__slot_size, r * self.__slot_size, self.__slot_size, self.__slot_size))

        #gets rectangle where pieces will spawn
        self.__origin = self.__slots[self.__slots_cols // 2]

    def draw(self):
        """
        Draws the grid

        Parameters
        ----------
        None
        """
        for recs in self.__slots:
            pygame.draw.rect(self.__screen, (57, 62, 70), recs, 2)

        #draws after so that it is on top
        pygame.draw.rect(self.__screen, (208, 220, 216), self.__outline, 2)
    
    def checkClear(self, placed):
        """
        Used to check if lines need to be cleared

        Parameters
        ----------
        placed : list
            The list of all shapes already placed down

        Returns
        -------
        int
            a number for a score
        """
        inRow = []

        #loops through each row and adds each part in that row to a list.
        #if the list is equal to the maximum size of the row destroy all parts in list.
        #then move all other shapes down one unit
        for r in range(self.__slots_rows):
            inRow.clear()
            for c in range(self.__slots_cols):
                for shapes in placed:
                    for part in shapes.getParts():
                        if self.__slots[r * self.__slots_cols + c].colliderect(part) == True:
                            inRow.append(part)
            if len(inRow) == self.__slots_cols:
                for part in inRow:
                    for shapes in placed:
                        if part in shapes.getParts():
                            shapes.getParts().remove(part)

                #move all shapes in above rows 1 down
                for shapes in placed:
                    for parts in shapes.getParts():
                        if parts.y < self.__slots[r * self.__slots_cols].y:
                            parts.y += self.__slot_size
                
                #plays sound for score
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('Audio/Line.mp3'))

                return 100
        
        return 0
                            
    def getOrigin(self):
        """
        gets the origin location of the grid

        Parameters
        ----------
        None

        Returns
        -------
        pygame.Rect
            The location where pieces spawn
        """
        return self.__origin

    def getSlotSize(self):
        """
        gets the size of the grid slots

        Parameters
        ----------
        None

        Returns
        -------
        int
            size of each grid slot 
        """
        return self.__slot_size

    def getOutline(self):
        """
        gets the outline shape of the grid

        Parameters
        ----------
        None

        Returns
        -------
        pygame.Rect
            a outline of the grid
        """
        return self.__outline