import pygame
import math
import snipets
import spritesheet


class Bullet(pygame.sprite.Sprite):
    def __init__(self, size, position, facing, shot_by, group):
        super().__init__(group)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.facing = facing
        self.shot_by = shot_by
        self.name = "gun"

    def update(self):
        self.move()
        self.collisions()

    def move(self):
        if self.facing == "right":
            self.rect.x += snipets.bullet_speed
        if self.facing == "left":
            self.rect.x -= snipets.bullet_speed

    def collisions(self):
        if pygame.sprite.spritecollide(self, snipets.platform_group, False):
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, size, position, facing, shot_by, group):
        super().__init__(group)
        bomb_image = snipets.bomb_image
        self.explosion_sound = pygame.mixer.Sound("Assets/explosion1.mp3")
        self.normal_image = spritesheet.get_sprite(bomb_image, 0, 0, 20, 26)
        self.normal_image = pygame.image.load("Assets/one_bomb.png")
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.facing = facing
        self.shot_by = shot_by
        self.dy = 0
        self.velocity_y = -5
        self.max_velocity = 1
        self.bounces = snipets.bomb_bounces
        self.time = snipets.bomb_explode_time
        self.angle = 0
        self.can_rotate = True
        self.exploding = False

        if self.facing == "left":
            self.dx = -5
        else: self.dx = 5

        self.explosion_image_list = []
        self.explosion_image_index = 0
        self.explosion_animation_timer = 0
        self.explosion_frame_speed = 3
        for i in range(11):
            image = spritesheet.get_sprite(pygame.image.load("Assets/Explosion.png"), i * 95, 0, 90, 96)
            self.explosion_image_list.append(image)
        self.dealt_damage = False
        self.name = "bomb"

    def update(self):
        self.rotate()
        self.movement()
        self.explode()
        self.time -= 1
        if self.time == 0:
            self.exploding = True



    def movement(self):
        if self.velocity_y > abs(self.max_velocity):
            if self.velocity_y < 0:
                self.velocity_y = -abs(self.max_velocity)

            if self.velocity_y > 0:
                self.velocity_y = abs(self.max_velocity)
        if not self.exploding:
            self.dy += self.velocity_y
            self.rect.x += self.dx
            self.wall_collisions("x")
            self.rect.y += self.dy
            self.wall_collisions("y")
            self.velocity_y += 1
    def wall_collisions(self, axis):
        hits = pygame.sprite.spritecollide(self, snipets.platform_group, False)
        if hits:
            platform = hits[0]
            if axis == "y":
                self.bounces -= 1
                if self.dy > 0:
                    self.rect.bottom = platform.rect.top
                    self.can_rotate = False
                elif self.dy < 0:
                    self.rect.top = platform.rect.bottom + 5
                if self.bounces > 0:
                    self.velocity_y = -3
                if self.bounces == 0:
                    self.dx = 0
                self.dy = 0
            if axis == "x":
                if self.dx > 0:
                    self.rect.right = platform.rect.left
                    self.dx = 0
                if self.dx < 0:
                    self.rect.left = platform.rect.right
                    self.dx = 0
    def explode(self):
        if self.exploding:
            if not self.dealt_damage:
                self.explosion_sound.play()
                for player in snipets.player_group:
                    distance = math.hypot(player.rect.centerx - self.rect.centerx,
                                player.rect.centery - self.rect.centery)
                    if distance < snipets.bomb_explosion_radius and not self.dealt_damage:
                        player.get_damage(snipets.bomb_damage)
                self.dealt_damage = True
                self.rect.x -= self.explosion_image_list[5].get_width() / 2
                self.rect.y -= self.explosion_image_list[5].get_height() /2
            if not self.explosion_image_index > len(self.explosion_image_list) - 1:
                if self.explosion_animation_timer >= self.explosion_frame_speed:
                    self.image = self.explosion_image_list[self.explosion_image_index]
                    self.explosion_image_index += 1
                    self.explosion_animation_timer = 0
                self.explosion_animation_timer += 1
            if self.explosion_image_index == len(self.explosion_image_list) - 1:
                self.kill()


    def rotate(self):
        if self.can_rotate:
            self.image = pygame.transform.rotate(self.normal_image, self.angle)
            self.angle += 10

class CannonBall(pygame.sprite.Sprite):
    def __init__(self, position, facing, shot_by, group):
        super().__init__(group)
        self.image = pygame.image.load("Assets/cannonball.png")
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.facing = facing
        self.dx = 0
        self.shot_by = shot_by
        self.name = "cannon"

    def update(self):
        if self.facing == "right":
            self.dx = snipets.cannonball_speed
        if self.facing == "left":
            self.dx = -snipets.cannonball_speed

        if pygame.sprite.spritecollide(self, snipets.platform_group, False):
            self.kill()

        self.rect.x += self.dx

class Mine(pygame.sprite.Sprite):
    def __init__(self, position, shot_by, group):
        super().__init__(group)
        self.explosion_sound = pygame.mixer.Sound("Assets/explosion1.mp3")
        self.image = snipets.weapons["mine"]["image"]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.dy = 0
        self.velocity_y = 0
        self.shot_by = shot_by
        self.name = "mine"
        self.exploding = False
        self.explosion_image_list = []
        self.explosion_image_index = 0
        self.explosion_animation_timer = 0
        self.explosion_frame_speed = 3
        for i in range(11):
            image = spritesheet.get_sprite(pygame.image.load("Assets/Explosion.png"), i * 95, 0, 90, 96)
            self.explosion_image_list.append(image)

        self.explosion_position_shifted = False

    def update(self):
        self.velocity_y = min(self.velocity_y + 1, 15)
        self.movement()

    def movement(self):
        if not self.exploding:
            self.dy = self.velocity_y
            self.collisions()
            self.rect.y += self.dy
        self.explode()

    def collisions(self):
        hits = pygame.sprite.spritecollide(self, snipets.platform_group, False)
        if hits:
            hit = hits[0]
            if self.dy > 0:
                if self.rect.colliderect(hit.rect):
                    self.rect.bottom = hit.rect.top
                    self.on_ground = True
                    self.velocity_y = 0
        else:
            self.velocity_y += 1
    def explode(self):
        if self.exploding:
            if not self.explosion_image_index > len(self.explosion_image_list) - 1:
                if self.explosion_animation_timer >= self.explosion_frame_speed:
                    self.image = self.explosion_image_list[self.explosion_image_index]
                    self.explosion_image_index += 1
                    self.explosion_animation_timer = 0
                self.explosion_animation_timer += 1
            if self.explosion_image_index == len(self.explosion_image_list) - 1:
                self.kill()

            if not self.explosion_position_shifted:
                self.rect.x -= self.explosion_image_list[5].get_width() / 2
                self.rect.y -= self.explosion_image_list[5].get_height() / 2
                self.explosion_position_shifted = True
                self.explosion_sound.play()

