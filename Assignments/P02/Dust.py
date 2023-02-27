#https://www.youtube.com/watch?v=nfJGJ98RW60&ab_channel=codeNULL
from Particle import Particle

class Dust:
    def __init__(self, pos, weight, color = (255,255,255)):
        self.__pos = pos
        self.__particles = []
        for i in range(weight):
            self.__particles.append(Particle(self.__pos, color))

    def update(self):
        for part in self.__particles:
            part.update()
            #remove particles that are to small to be seen
            self.__particles = [particle for particle in self.__particles if particle.radius > 0]

    def draw(self, win):
        for i in self.__particles:
            i.draw(win)