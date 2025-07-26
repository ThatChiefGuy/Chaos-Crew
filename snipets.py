import pygame

import snipets
import spritesheet


screen_size_x = 800
screen_size_y = 600
player_movement_speed = 5
player_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
gravity = 1
player_jump_strength = 20
fps = 60
tile_size_x = 32
tile_size_y = 24
bullet_speed = 25
enemy_speed = 5
pickup_group = pygame.sprite.Group()
pickup_spawn_time = 150
pickup_types = ["health", "weapon", "speed", "shield"]
shield_pickup_duration = 150
speed_duration = 400
speed_multiplier = 2
player_health = 100
health_pickup_strength = 20
bomb_damage = 60
bomb_bounces = 2
bomb_explode_time = 80
bomb_explosion_radius = 100
shield_timer = 100
shieled_cooldown = 400
player_images = []
for i in range(4):
    player_images.append(spritesheet.get_sprite(pygame.image.load("Assets/player_spritesheet.png"), i * 39, 0, 39, 37))
player_animation_framerate = 8
map = [
    ".........................",
    ".........................",
    ".........................",
    ".........................",
    ".........................",
    ".........................",
    "........LWWWWWWWR........",
    ".........................",
    ".........................",
    ".........................",
    ".........................",
    "..LWWWWWR.......LWWWWWR..",
    ".........................",
    ".........................",
    ".........................",
    ".........................",
    ".........................",
    "........LWWWWWWWR........",
    ".........................",
    ".........................",
    ".........................",
    ".........................",
    ".LWWWWWWWR....LWWWWWWWWR.",
    ".........................",
    ".........................",
]
bomb_ammo = 5
bomb_cooldown = 100
crates = ["bomb", "gun", "cannon", "mine"]
gun_image = pygame.image.load("Assets/gun.png")
bomb_image = pygame.image.load("Assets/bomb.png")
one_bomb_image = pygame.image.load("Assets/one_bomb.png")
shield_image = pygame.image.load("Assets/shield.png")
kick_reach = 50
kick_damage = 10
kick_cooldown = 20
player_kick_image = pygame.image.load("Assets/player_kick_image.png")
weapons = {"gun":
               {"damage": 15,
                "ammo": 20,
                "cooldown": 20,
                "image": pygame.image.load("Assets/gun.png")
                },
           "bomb":
               {"damage": 0,
                "ammo": 5,
                "cooldown": 20,
                "image": pygame.image.load("Assets/bomb.png")
                },
            "cannon":
                    {"damage": 90,
                     "ammo": 3,
                     "cooldown": 100,
                     "image": pygame.image.load("Assets/cannon2.png")},
           "mine":
               {"damage": 50,
                     "ammo": 3,
                     "cooldown": 50,
                     "image": pygame.image.load("Assets/mine.png")}
                }
cannonball_speed = 40
grass_tile_image = spritesheet.get_sprite(pygame.image.load("Assets/Tileset_ground.png"),
                                          32, 96, snipets.tile_size_x, snipets.tile_size_y)
grass_tile_left_image = spritesheet.get_sprite(pygame.image.load("Assets/Tileset_ground.png"),
                                               0, 96, snipets.tile_size_x, snipets.tile_size_y)

grass_tile_right_image = spritesheet.get_sprite(pygame.image.load("Assets/Tileset_ground.png"),
                                                95, 96, snipets.tile_size_x, snipets.tile_size_y)