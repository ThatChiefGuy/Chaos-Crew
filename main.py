import pygame
import random
import pickup
import platform
import player
import snipets
import spritesheet
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((snipets.screen_size_x, snipets.screen_size_y))
player1 = player.Player((32,  32) , (200, 200), snipets.player_group, [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE, pygame.K_e])
player2 = player.Player((20, 40), (600, 200), snipets.player_group, [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_KP0, pygame.K_KP1])
heart_sprite_sheet = pygame.image.load("Assets/heartshealth.png")
heart_images = []
heart_position_y = 7
heart5 = spritesheet.get_sprite(heart_sprite_sheet, 5, 7, 205, 35)
heart4 = spritesheet.get_sprite(heart_sprite_sheet, 5, 52, 205, 35)
heart3 = spritesheet.get_sprite(heart_sprite_sheet, 5, 96, 205, 35)
heart2 = spritesheet.get_sprite(heart_sprite_sheet, 5, 133, 205, 35)
heart1 = spritesheet.get_sprite(heart_sprite_sheet, 5, 170, 205, 35)
heart0 = spritesheet.get_sprite(heart_sprite_sheet, 5, 208, 205, 35)
pygame.mixer.music.load("Assets/Cyborg_Factory_Fight.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)
run = True
pickup_spawn_time = snipets.pickup_spawn_time

def draw_weapon(player):
    if not player.weapon is None:
        if player.facing == "left":
            image = snipets.weapons[player.weapon]["image"]
            window.blit(image, (player.rect.centerx - image.get_width(), player.rect.centery - image.get_height() / 2))
        else:
            image = pygame.transform.flip(snipets.weapons[player.weapon]["image"], True, False)
            window.blit(image, (player.rect.centerx, player.rect.centery - image.get_height() / 2))

    if player.shield_on:
        window.blit(snipets.shield_image, (player.rect.centerx - snipets.shield_image.get_width() / 2,
                                               player.rect.centery - snipets.shield_image.get_height() / 2))

def on_restart():
    player1.lives = 5
    player2.lives = 5
    player1.health = snipets.player_health
    player2.health = snipets.player_health
    player1.weapon = None
    player2.weapon = None
    valid_position = False
    while not valid_position:
        position = random.randint(0, snipets.screen_size_x), 0
        for platform in snipets.platform_group:
            if position[0] > platform.rect.left and position[0] < platform.rect.right:
                valid_position = True
                break
            else:
                valid_position = False
    player1.rect.center = position
    valid_position = False
    while not valid_position:
        position = random.randint(0, snipets.screen_size_x), 0
        for platform in snipets.platform_group:
            if position[0] > platform.rect.left and position[0] < platform.rect.right:
                valid_position = True
                break
            else:
                valid_position = False
    player2.rect.center = position
    player1.speed_multiplier = 1
    player2.speed_multiplier = 1
    for sprite in snipets.weapon_group:
        sprite.kill()

def end_game():
    font = pygame.font.Font('Assets/arcadeclassic/ARCADECLASSIC.TTF', 100)
    text = font.render(' ', True, "black")
    text_rect = text.get_rect()
    text_rect.center = (snipets.screen_size_x // 2, snipets.screen_size_y // 4)
    mouse_position = pygame.mouse.get_pos()
    restart_image = None

    if player1.lives == 0:
        font = pygame.font.Font('Assets/arcadeclassic/ARCADECLASSIC.TTF', 100)
        text = font.render('Player 2 won!', True, "black")
        text_rect = text.get_rect()
        text_rect.center = (snipets.screen_size_x // 2, snipets.screen_size_y // 4)
        restart_image = pygame.image.load("Assets/restart_button.png")
        restart_button_rect = restart_image.get_rect()
        restart_button_rect.center = (snipets.screen_size_x // 2, snipets.screen_size_y // 2)
        if restart_button_rect.collidepoint(mouse_position) and pygame.mouse.get_pressed()[0]:
            on_restart()

    if player2.lives == 0:
        font = pygame.font.Font('Assets/arcadeclassic/ARCADECLASSIC.TTF', 100)
        text = font.render('Player 1 won!', True, "black")
        text_rect = text.get_rect()
        text_rect.center = (snipets.screen_size_x // 2, snipets.screen_size_y // 4)
        restart_image = pygame.image.load("Assets/restart_button.png")
        restart_button_rect = restart_image.get_rect()
        restart_button_rect.center = (snipets.screen_size_x // 2, snipets.screen_size_y // 2)
        if restart_button_rect.collidepoint(mouse_position) and pygame.mouse.get_pressed()[0]:
            on_restart()
    return text, text_rect, restart_image

def handle_lives():
    player1_hearts_image = heart1
    player2_hearts_image = heart1
    if player1.lives == 5:
        player1_hearts_image = heart5
    if player1.lives == 4:
        player1_hearts_image = heart4
    if player1.lives == 3:
        player1_hearts_image = heart3
    if player1.lives == 2:
        player1_hearts_image = heart2
    if player1.lives == 1:
        player1_hearts_image = heart1
    if player1.lives == 0:
        player1_hearts_image = heart0


    if player2.lives == 5:
        player2_hearts_image = heart5

    if player2.lives == 4:
        player2_hearts_image = heart4

    if player2.lives == 3:
        player2_hearts_image = heart3

    if player2.lives == 2:
        player2_hearts_image = heart2

    if player2.lives == 1:
        player2_hearts_image = heart1

    if player2.lives == 0:
        player2_hearts_image = heart0

    return player1_hearts_image, player2_hearts_image

def draw_map():
    for y, row in enumerate(snipets.map):
        for x, character in enumerate(row):
            if character == "W":
                platform.Platform((snipets.tile_size_x, snipets.tile_size_y), (x * snipets.tile_size_x, y * snipets.tile_size_y), snipets.platform_group, snipets.grass_tile_image)
            if character == "L":
                platform.Platform((snipets.tile_size_x, snipets.tile_size_y), (x * snipets.tile_size_x, y * snipets.tile_size_y), snipets.platform_group, snipets.grass_tile_left_image)
            if character == "R":
                platform.Platform((snipets.tile_size_x, snipets.tile_size_y), (x * snipets.tile_size_x, y * snipets.tile_size_y), snipets.platform_group, snipets.grass_tile_right_image)
player1_health_outline = pygame.Rect(30, 30, snipets.player_health * 2, 20)
player2_health_outline = pygame.Rect(snipets.screen_size_x - 30 - snipets.player_health * 2, 30, snipets.player_health * 2, 20)
player1_shield = pygame.Rect(30, 30, player1.shield_timer * 2, 100)
player2_shield = pygame.Rect(snipets.screen_size_x - 30 - player2.shield_timer * 2, 30, player2.shield_timer * 2, 100)

def draw(player1_hearts_image, player2_hearts_image, end_text, end_text_rect, restart_image):
    window.fill("cyan")

    snipets.player_group.draw(window)
    snipets.platform_group.draw(window)
    snipets.weapon_group.draw(window)
    snipets.enemy_group.draw(window)
    snipets.pickup_group.draw(window)

    window.blit(player1_hearts_image,(30, 100))
    window.blit(player2_hearts_image,(snipets.screen_size_x - player1_health_outline.width - 30, 100))

    pygame.draw.rect(window, "blue", player1_health_outline, 2)
    pygame.draw.rect(window, "red", player2_health_outline, 2)
    player1_health = pygame.Rect(32, 32, player1.health * 2 - 4, 15)
    player2_health = pygame.Rect(snipets.screen_size_x - 32 - snipets.player_health * 2 + 4, 32, player2.health * 2 - 4, 15)
    player1_shield = pygame.Rect(30, 70, player1.shield_timer * 2, 14)
    player2_shield = pygame.Rect(snipets.screen_size_x - 30 - player2.shield_timer * 2, 70, player2.shield_timer * 2, 14)
    pygame.draw.rect(window, "green", player1_health)
    pygame.draw.rect(window, "green", player2_health)
    pygame.draw.rect(window, "blue", player1_shield)
    pygame.draw.rect(window, "blue", player2_shield)
    draw_weapon(player1)
    draw_weapon(player2)
    window.blit(end_text, end_text_rect)
    if not restart_image is None:
        window.blit(restart_image, (snipets.screen_size_x // 2 - restart_image.get_width() / 2, snipets.screen_size_y // 2 - restart_image.get_height() / 2))
    player1_rect = pygame.Rect(player1.rect.centerx, player1.rect.top - 20, 10, 10)
    player2_rect = pygame.Rect(player2.rect.centerx, player2.rect.top - 20, 10, 10)
    pygame.draw.rect(window, "blue", player1_rect)
    pygame.draw.rect(window, "red", player2_rect)
    pygame.display.update()


clock = pygame.time.Clock()
draw_map()
while run:
    clock.tick(snipets.fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if player1.lives > 0 and player2.lives > 0:
        snipets.player_group.update()
        snipets.weapon_group.update()
        snipets.enemy_group.update(player)
        snipets.pickup_group.update()
        player1_hearts_image, player2_hearts_image = handle_lives()
    pickup_spawn_time -= 1
    if pickup_spawn_time <= 0:
        pickup.Pickup((32, 32), (random.randint(20, 780), 0), snipets.pickup_group)
        pickup_spawn_time = snipets.pickup_spawn_time
    end_text, end_text_rect, restart_image = end_game()
    draw(player1_hearts_image, player2_hearts_image, end_text, end_text_rect, restart_image)

