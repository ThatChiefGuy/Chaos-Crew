import pygame

def get_sprite(spritesheet, x, y, width, height):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(spritesheet, (0, 0), pygame.Rect(x, y, width, height))
    return image
