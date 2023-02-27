#https://www.youtube.com/watch?v=nfJGJ98RW60&ab_channel=codeNULL
import pygame
import random

class Particle:
    def __init__(self, pos, color):
        self.x, self.y = pos
        self.vx, self.vy = random.randint(-2, 2), random.randint(-10, 0)*.1
        self.radius = 7
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if random.randint(0, 100) < 40:
            self.radius -= 1