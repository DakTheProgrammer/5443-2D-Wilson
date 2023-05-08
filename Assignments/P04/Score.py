import pygame

class Score:
    """
    Score class is a container for the score.

    Attributes
    ----------
    __font : pygame.font.Font
        The font
    __score : int   
        The score
    
    Methods
    -------
    draw(screen, left, top)
        Draws the score
    update(score)
        Updates the score
    """
    def __init__(self):
        """
        Constructor for Score class that is a container for the score.
        """
        self.__font = pygame.font.Font('Assets/Font/dungeon.ttf', 32)
        self.__score = 0
        
    def update(self, score):
        """
        Updates the score.

        Args:
            score (int): The score of the player
        """
        self.__score = score
        
    def draw(self, screen, left, top):
        """
        Draws the score to the screen.

        Args:
            screen (Surface): The screen to draw on
            left (int): the left side of the screen
            top (int): the top of the screen
        """
        screen.blit(self.__font.render("SCORE " + str(self.__score), 1, (205,170,150)),(left, top))
  
        