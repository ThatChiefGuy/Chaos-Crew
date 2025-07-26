import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, size, position, group, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position

