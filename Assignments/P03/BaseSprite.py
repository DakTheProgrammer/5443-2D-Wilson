import pygame
import Util

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, img, size, mask = False, loc = (0,0)):
        super().__init__()

        self.image = img
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft = loc)
        
        #used to make transitions look smoother
        self.rectBuffer = self.image.get_size()[1] / 2

        #needed for rotation
        self.imageHolder = self.image

        if mask == True:
            self.__mask = pygame.mask.from_surface(self.image)
        else:
            self.__mask = None

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255,0,0), self.rect, 1)
        
        # if (self.__mask != None):
        #     pygame.draw.lines(screen, (0,255,0), (100,100), self.__mask.outline())

    def setImage(self, img, scale):
        self.image = pygame.transform.scale(img, Util.scale(img.get_size(), scale))
        
    def update(self, cmd, arg, ret = None):
        if cmd == 'Location':
            self.rect.center = arg
        elif cmd == 'Rotate':
            imageRect = self.imageHolder.get_rect(center = self.rect.center)

            self.image = pygame.transform.rotate(self.imageHolder, arg)
            self.rect = self.image.get_rect(center = imageRect.center)
        elif cmd == 'Move':
            self.rect.center += arg[0]
            if self.rect.top <= -self.rectBuffer:
                self.rect.bottom = arg[1].get_height() + self.rectBuffer
            elif self.rect.left <= -self.rectBuffer:
                self.rect.right = arg[1].get_width() + self.rectBuffer
            elif self.rect.bottom >= arg[1].get_height() + self.rectBuffer:
                self.rect.top = -self.rectBuffer
            elif self.rect.right >= arg[1].get_width() + self.rectBuffer:
                self.rect.left = -self.rectBuffer
        elif cmd == 'Collide':
            #how to check for collisions
            offset = (arg[1][0] - self.rect[0], arg[1][1] - self.rect[1])
            overlaps = self.__mask.overlap(arg[0], offset)
            
            if overlaps:
                ret[0] = True
                
    def getMask(self):
        return self.__mask