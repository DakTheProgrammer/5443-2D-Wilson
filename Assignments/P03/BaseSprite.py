import pygame

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, img, size, mask = False):
        super().__init__()

        self.image = img
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

        if mask == True:
            ...
        else:
            ...

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        #hmmm
        return super().update()