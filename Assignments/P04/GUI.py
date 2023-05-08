from HealthBar import HealthBar
from Score import Score
class GUI:
    """
    GUI class is a container for the health bar and score.

    Attributes
    ----------
    __healthBar : HealthBar
        The health bar
    __score : Score
        The score
    """
    def __init__(self, sheet):
        """
        Constructor for GUI class that takes in a sprite sheet.
        Then creates a health bar and score.

        Args:
            sheet (SpriteSheet): The sprite sheet
        """
        self.__healthBar = HealthBar(sheet)
        self.__score = Score()
        
    def update(self, health, score):
        """
        Updates the health bar and score.

        Args:
            health (int): The health of the player
            score (int): The score of the player
        """
        self.__score.update(score)
        self.__healthBar.update(health)
        
    def draw(self, screen, left, top):
        """
        Draws the health bar and score.

        Args:
            screen (Surface): the screen to draw on
            left (int): the left side of the screen
            top (int): the top of the screen
        """
        self.__score.draw(screen, (left+16), (top + 16))
        self.__healthBar.draw(screen, (left+16), (top+48))
        
   