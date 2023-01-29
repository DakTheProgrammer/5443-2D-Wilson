import pygame

class Grid:

    def __init__(self, screen):
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
        for recs in self.__slots:
            pygame.draw.rect(self.__screen, (57, 62, 70), recs, 2)

        #draws after so that it is on top
        pygame.draw.rect(self.__screen, (208, 220, 216), self.__outline, 2)
    
    def checkClear(self, placed):
        inRow = []
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
                
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('Audio/Line.mp3'))

                return 100
        
        return 0

    def checkGameOver(self, placed):
        pass
                            
    def getOrigin(self):
        return self.__origin

    def getSlotSize(self):
        return self.__slot_size

    def getOutline(self):
        return self.__outline