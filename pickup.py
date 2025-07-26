import pygame
import random
import snipets


class Pickup(pygame.sprite.Sprite):
    def __init__(self, size, position, group):
        super().__init__(group)

        self.image = pygame.Surface(size)
        self.image = pygame.image.load("Assets/wooden_box.png")
        self.type = random.choice(snipets.pickup_types)
        self.type = "shield"
        if self.type == "shield":
            shield = pygame.transform.scale(pygame.image.load("Assets/shield.png"), (25, 25))
            self.image.blit(shield, (self.image.get_width() / 2 - shield.get_width() / 2, self.image.get_height() / 2 - shield.get_height() / 2))
        if self.type == "weapon":
            self.weapon = random.choice(snipets.crates)
            self.image.blit(snipets.weapons[self.weapon]["image"],(self.image.get_width() / 2 - snipets.weapons[self.weapon]["image"].get_width() / 2, self.image.get_height() / 2 - snipets.weapons[self.weapon]["image"].get_height() / 2))

        elif self.type == "health":
            self.image = pygame.image.load("Assets/pickup_image.png")
        elif self.type == "speed":
            self.image = pygame.image.load("Assets/speed_pickup_image.png")

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.dy = 0
        self.velocity_y = snipets.gravity


    def update(self):
        self.movement()
        self.collisions()

    def movement(self):
        self.dy += self.velocity_y
        self.rect.y += self.dy

    def collisions(self):
        platform_hits = pygame.sprite.spritecollide(self, snipets.platform_group, False)
        if platform_hits:
            platform = platform_hits[0]
            self.rect.bottom = platform.rect.top
            self.velocity_y = 0
        else:
            self.velocity_y = snipets.gravity
