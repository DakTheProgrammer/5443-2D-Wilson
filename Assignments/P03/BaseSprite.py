import pygame
from pygame.math import Vector2

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, img, size, mask = False, loc = (0,0)):
        super().__init__()

        self.image = img
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft = loc)
        
        #used to make transitions look smoother
        self.rectBuffer = self.image.get_size()[1] / 2

        if mask == True:
            ...
        else:
            ...

    def update(self, cmd, arg, ret = None):
        if cmd == 'Location':
            self.rect.center = arg
        elif cmd == 'Rotate':
            #rotate :)
            ...
        elif cmd == 'Move':
            self.rect.center += arg[0]
            if self.rect.top <= -self.rectBuffer:
                self.rect.bottom = arg[1].get_height() + self.rectBuffer
            elif self.rect.left <= -self.rectBuffer:
                self.rect.right = arg[1].get_width() + self.rectBuffer
            elif self.rect.bottom >= arg[1].get_height() + self.rectBuffer:
                #move to top
                self.rect.top = -self.rectBuffer
            elif self.rect.right >= arg[1].get_width() + self.rectBuffer:
                #move to left side
                self.rect.left = -self.rectBuffer