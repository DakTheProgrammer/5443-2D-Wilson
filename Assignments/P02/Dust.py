
from Particle import Particle
"""
    A class used to represent the particles in a dust like pattern
    used as trail for projectile, fire, and tank shooting

    This was edited from https://www.youtube.com/watch?v=nfJGJ98RW60&ab_channel=codeNULL
    ...

    Attributes
    ----------
    
    pos : tuple
        the location of the dust
    particles : list
        the particles inside the dust

    Methods
    -------
    draw()
        draws all the items on screen
    update(event):
        handles the events sent to the game

    """
class Dust:
    def __init__(self, pos, weight, color = (255,255,255)):
        """
        Parameters
        ----------
        pos : tuple
            location of dust
        weight : int
            amount of particles in dust
        color (optional): tuple
            color of particles
        """
        self.__pos = pos
        self.__particles = []
        for i in range(weight):
            self.__particles.append(Particle(self.__pos, color))

    def update(self):
        """
        scatters the particles in the list

        Parameters
        ----------
        """
        for part in self.__particles:
            part.update()
            #remove particles that are to small to be seen
            self.__particles = [particle for particle in self.__particles if particle.radius > 0]

    def draw(self, screen):
        """
        draws all particles

        Parameters
        ----------
        screen : pygame.display
            the screen of the game to draw on
        """
        for i in self.__particles:
            i.draw(screen)