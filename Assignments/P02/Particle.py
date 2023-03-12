#https://www.youtube.com/watch?v=nfJGJ98RW60&ab_channel=codeNULL
import pygame
import random
"""
    A class used to represent the particles for dust

    This was edited from https://www.youtube.com/watch?v=nfJGJ98RW60&ab_channel=codeNULL
    ...

    Attributes
    ----------
    
    x : int
        x location of tuple
    y : int
        y location of tuple
    vx : int
        velocity in x direction
    vy : int
        velocity in y direction
    radius : int
        size of particle
    color : tuple
        color of the particle

    Methods
    -------
    draw(screen)
        draws the given particle on screen
    update():
        updates the position of the particle

    """

class Particle:
    def __init__(self, pos, color):
        """
        Parameters
        ----------
        pos : tuple
            the location of the particle
        color : tuple
            the RGB color of the particle
        """
        self.x, self.y = pos
        self.vx, self.vy = random.randint(-2, 2), random.randint(-10, 0)*.1
        self.radius = 7
        self.color = color

    def draw(self, screen):
        """
        draws the given particle

        Parameters
        ----------
        screen : pygame.display
            the screen used by pygame

        """
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def update(self):
        """
        updates the position of the particle using its velocity
        and shirking it occasionally

        Parameters
        ----------
        """
        self.x += self.vx
        self.y += self.vy
        if random.randint(0, 100) < 40:
            self.radius -= 1