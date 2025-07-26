import spritesheet
import snipets
import pygame
import weapons
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, size: (int, int), position: (int, int), group, controls):
        super().__init__(group)
        self.controls = controls
        self.normal_image = spritesheet.get_sprite(pygame.image.load("Assets/player_spritesheet.png"), 0 , 0, 39, 37)
        self.image = self.normal_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.velocity_y = 0
        self.velocity_x = 0
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        self.facing = "right"
        self.can_shoot = True
        self.health = snipets.player_health
        self.max_health = snipets.player_health
        self.weapon = "gun"
        self.shield_on = False
        self.shield_timer = snipets.shield_timer
        self.shield_image = pygame.image.load("Assets/shield.png")
        self.shield_image = pygame.transform.scale(self.shield_image, self.normal_image.get_size())
        self.can_shield = True
        self.shield_cooldown = snipets.shieled_cooldown
        self.lives = 5
        self.animation_timer = 0
        if not self.weapon is None:
            self.shooting_cooldown = snipets.weapons[self.weapon]["cooldown"]
            self.ammo = snipets.weapons[self.weapon]["ammo"]
        else:
            self.ammo = 0
            self.shooting_cooldown = 0
        self.animation_index = 0
        self.kick_timer = snipets.kick_cooldown
        self.kick_animation_timer = -1
        self.kicking = False
        self.speed_duration = 0
        self.speed_multiplier = 1

        self.cannon_sound = pygame.mixer.Sound("Assets/cannon_fire.mp3")
        self.cannon_sound.set_volume(2.0)
        self.gun_sound = pygame.mixer.Sound("Assets/gun_shot.mp3")
        self.box_break_sound = pygame.mixer.Sound("Assets/box_break_sound.mp3")
        self.box_break_sound.set_volume(0.5)

    def update(self):
        self.pickup_collisions()
        self.movement()
        self.jump()
        self.weapon_collisions()
        self.shoot()
        self.shield()
        self.kick()
        self.animation()
        self.dx = 0

    def kick(self):
        keys_pressed = pygame.key.get_pressed()
        self.kick_timer -= 1
        if self.kick_animation_timer > 0:
            self.kick_animation_timer -= 1
        if self.kick_animation_timer == 0:
            self.kicking = False
            if self.facing == "right":
                self.image = self.normal_image.copy()
            else:
                self.image = pygame.transform.flip(self.normal_image, True, False)
            self.kick_animation_timer = -1
        if keys_pressed[self.controls[5]] and self.kick_timer <= 0:
            self.kicking = True
            self.kick_animation_timer = 10
            if self.facing == "right":
                self.image = snipets.player_kick_image
                for player in snipets.player_group:
                    if abs(self.rect.y - player.rect.y) < 10:
                        distance_x = self.rect.right - player.rect.right
                        if not player == self:
                            if abs(distance_x) < snipets.kick_reach and distance_x < 0:
                                player.get_damage(snipets.kick_damage)

            if self.facing == "left":
                self.image = pygame.transform.flip(snipets.player_kick_image, True, False)
                for player in snipets.player_group:
                    if abs(self.rect.y - player.rect.y) < 10:
                        distance_x = self.rect.right - player.rect.right
                        if not player == self:
                            if abs(distance_x) < snipets.kick_reach and distance_x > 0:
                                player.get_damage(snipets.kick_damage)
            self.kick_timer = snipets.kick_cooldown
    def movement(self):
        keys = pygame.key.get_pressed()
        self.speed_multiplier = snipets.speed_multiplier if self.speed_duration > 0 else 1
        if keys[self.controls[1]] and not self.shield_on:
            self.facing = "left"
            self.dx = -snipets.player_movement_speed * self.speed_multiplier
        if keys[self.controls[3]] and not self.shield_on:
            self.facing = "right"
            self.dx = snipets.player_movement_speed * self.speed_multiplier

        self.dy = self.velocity_y
        self.dx += self.velocity_x
        self.rect.y += self.dy
        self.wall_collisions("y")
        self.rect.x += self.dx
        self.wall_collisions("x")
        if self.velocity_x > 0:
            self.velocity_x -= 1
        if self.velocity_x < 0:
            self.velocity_x += 1

        if self.speed_duration > 0:
            self.speed_duration -= 1

    def wall_collisions(self, axis):
        hits = pygame.sprite.spritecollide(self, snipets.platform_group, False)

        if hits:
            hit = hits[0]
            if axis == "y":
                if self.dy > 0:
                    if self.rect.colliderect(hit.rect):
                        self.rect.bottom = hit.rect.top
                        self.on_ground = True
                        self.velocity_y = 0
                elif self.dy < 0:
                    if self.rect.colliderect(hit.rect):
                        self.rect.top = hit.rect.bottom
                        self.velocity_y = 0
            if axis == "x":
                if self.dx > 0:
                    if self.rect.right > hit.rect.left:
                        self.rect.right = hit.rect.left
                if self.dx < 0:
                    if self.rect.left < hit.rect.right:
                        self.rect.left = hit.rect.right
        else:
            if axis == "y":
                self.velocity_y += snipets.gravity
                self.on_ground = False
        if self.rect.top > snipets.screen_size_y:
            self.get_damage(snipets.player_health)


    def jump(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[self.controls[0]] and self.on_ground == True and not self.shield_on:
            self.velocity_y = -snipets.player_jump_strength

    def shoot(self):
        keys_pressed = pygame.key.get_pressed()

        if self.ammo <= 0:
            self.can_shoot = False
            self.weapon = None

        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1
        else:
            self.can_shoot = True

        if self.shield_on:
            self.can_shoot = False

        if keys_pressed[self.controls[4]] and self.can_shoot:
            if self.weapon == "gun":
                self.gun_sound.play()
                weapons.Bullet((5, 2), self.rect.center, self.facing, self, snipets.weapon_group)

            if self.weapon == "bomb" and self.can_shoot:
                weapons.Bomb((15, 15), self.rect.center, self.facing, self, snipets.weapon_group)

            if self.weapon == "mine" and self.can_shoot:
                weapons.Mine(self.rect.center, self, snipets.weapon_group)

            if self.weapon == "cannon" and self.can_shoot:
                weapons.CannonBall(self.rect.center, self.facing, self, snipets.weapon_group)
                self.cannon_sound.play()
                if self.facing == "right" and not self.shield_on:
                    self.velocity_x = -23
                if self.facing == "left" and not self.shield_on:
                    self.velocity_x = 23

            self.can_shoot = False
            if not self.weapon == None:
                self.shooting_cooldown = snipets.weapons[self.weapon]["cooldown"]
            self.ammo -= 1


    def weapon_collisions(self):
        weapon = pygame.sprite.spritecollide(self, snipets.weapon_group, False)
        if weapon:
            if not weapon[0].shot_by == self and not type(weapon[0]) == weapons.Bomb and not type(weapon[0]) == weapons.Mine:
                self.get_damage(snipets.weapons[weapon[0].name]["damage"])
                if type(weapon[0]) == weapons.CannonBall:
                    if weapon[0].facing == "right" and not self.shield_on:
                        self.velocity_x = 27
                    if weapon[0].facing == "left" and not self.shield_on:
                        self.velocity_x = -27
                weapon[0].kill()
            if type(weapon[0]) == weapons.Mine and not weapon[0].shot_by == self:
                if not weapon[0].exploding:
                    self.get_damage(snipets.weapons["mine"]["damage"])
                weapon[0].exploding = True

    def get_damage(self, amount):
        if not self.shield_on:
            self.health -= amount
        if self.health <= 0:
            if self.lives > 0:
                death_sound = pygame.mixer.Sound("Assets/death sound effect/" + str(random.randint(1, 19)) + ".mp3")
                self.lives -= 1
                death_sound.play()
                if not self.lives == 0:
                    self.health = snipets.player_health
                    valid_position = False
                    while not valid_position:
                        position = random.randint(0, snipets.screen_size_x), 0
                        for platform in snipets.platform_group:
                            if position[0] > platform.rect.left and position[0] < platform.rect.right:
                                valid_position = True
                                break
                            else:
                                valid_position = False
                    self.rect.center = position
            if self.lives == 0:
                self.weapon = None


    def get_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def pickup_collisions(self):
        pickup_hit = pygame.sprite.spritecollide(self, snipets.pickup_group, False)
        if pickup_hit:
            self.box_break_sound.play()
            pickup = pickup_hit[0]
            if pickup.type == "health":
                self.get_health(snipets.health_pickup_strength)

            if pickup.type == "weapon":
                if pickup.weapon == self.weapon:
                    self.ammo = snipets.weapons[self.weapon]["ammo"]
                else:
                    self.weapon = pickup.weapon
                    self.ammo = snipets.weapons[self.weapon]["ammo"]
            if pickup.type == "speed":
                self.speed_duration = snipets.speed_duration
            pickup.kill()
    def shield(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[self.controls[2]] and self.can_shield:
            self.shield_timer -= 1
            self.shield_on = True

            if self.shield_timer == 0:
                self.can_shield = False
                self.shield_on = False
                self.shield_cooldown = snipets.shieled_cooldown

        else:
            self.shield_on = False


        if not self.can_shield:
            self.shield_cooldown -= 1
            if self.shield_cooldown <= 0:
                self.can_shield = True
                self.shield_timer = snipets.shield_timer

    def animation(self):
        if not self.kicking:
            if not self.dx == 0:
                if self.animation_timer >= snipets.player_animation_framerate:
                    if self.facing == "right":
                        self.image = snipets.player_images[self.animation_index]
                        self.animation_index = (self.animation_index + 1) % len(snipets.player_images)
                        self.animation_timer = 0
                    if self.facing == "left":
                        self.image = pygame.transform.flip(snipets.player_images[self.animation_index], True, False)
                        self.animation_index = (self.animation_index + 1) % len(snipets.player_images)
                        self.animation_timer = 0
                self.animation_timer += 1
