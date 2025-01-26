import pygame
import math
from random import randint

pygame.init()

screenWidth = 1400
screenHeight = 720
clock = pygame.time.Clock()

main = True

ammo_count = 3  # Initial ammo count
gravity = 0.5  # Gravity pulling the player down

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Duck Shot')

ammo_sprite = pygame.image.load(r"C:\Users\debra\.vscode\DuckShot\DuckShot_ammo.png")

click = False

def spawn_ammo():
    ammo_positions = []
    ammo_sprites = []
    for _ in range(randint(1, 6)):  # Spawn between 1 and 6 ammo
        ammo_rect = ammo_sprite.get_rect(center=(randint(100, screenWidth - 100), randint(100, screenHeight - 100)))
        ammo_positions.append(ammo_rect)
        ammo_sprites.append(ammo_sprite)
    return ammo_positions, ammo_sprites

ammo_positions, ammo_sprites = spawn_ammo()

player = pygame.image.load(r'C:\Users\debra\.vscode\DuckShot\Duckshot_player.png')
player = pygame.transform.scale(player, (player.get_width() * 3, player.get_height() * 3))
player_rect = player.get_rect(center=(screenWidth // 2, screenHeight // 2))  # Center the player

gun = pygame.image.load(r'C:\Users\debra\.vscode\DuckShot\Duckshot_Gun.png')
gun = pygame.transform.scale(gun, (gun.get_width() * 2, gun.get_height() * 2))

def drawMainMenu():
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 200)
    main_text = font.render('Duck Shot ', True, (0, 0, 0))
    screen.blit(main_text, (screenWidth // 2 - 350 , 100))

    font = pygame.font.Font(None, 100)
    EasyMode = font.render('Easy Mode ', True, (0, 0, 0))
    EasyMode_rect = EasyMode.get_rect(center=(screenWidth // 2, screenHeight // 2))
    screen.blit(EasyMode, EasyMode_rect)

    MediumMode = font.render('Medium Mode ', True, (0, 0, 0))
    MediumMode_rect = MediumMode.get_rect(center=(screenWidth // 2, screenHeight // 2 + 100))
    screen.blit(MediumMode, MediumMode_rect)

    HardMode = font.render('Hard Mode ', True, (0, 0, 0))
    HardMode_rect = HardMode.get_rect(center=(screenWidth // 2, screenHeight // 2 + 200))
    screen.blit(HardMode, HardMode_rect)

    mouse_pos = pygame.mouse.get_pos()

    # Handle button clicks
    global gravity
    if pygame.Rect(EasyMode_rect).collidepoint(mouse_pos):
        if click:
            gravity = 0.3
            start_game()
    elif pygame.Rect(MediumMode_rect).collidepoint(mouse_pos):
        if click:
            gravity = 0.5
            start_game()
    elif pygame.Rect(HardMode_rect).collidepoint(mouse_pos):
        if click:
            gravity = 0.7
            start_game()

def start_game():
    global main
    main = False

def draw_ammo_count():
    font = pygame.font.Font(None, 100)
    text = font.render(f'{ammo_count}', True, (255, 255, 255))
    screen.blit(text, (screenWidth // 2 - 50, screenHeight // 2 - 300))

def draw_game_over():
    font = pygame.font.Font(None, 72)
    text = font.render('You Died!', True, (0, 0, 0))
    screen.blit(text, (screenWidth//2 , screenHeight))

def draw_buttons():
    font = pygame.font.Font(None, 72)
    restart_button = font.render('Restart', True, (0, 0, 0))
    exit_button = font.render('Exit Game', True, (0, 0, 0))
    restart_rect = restart_button.get_rect(center=(screenWidth//2, screenHeight//2 + 75))
    exit_rect = exit_button.get_rect(center=(screenWidth//2, screenHeight//2 + 150))
    screen.blit(restart_button, restart_rect)
    screen.blit(exit_button, exit_rect)
    return restart_rect, exit_rect

def game():
    global ammo_count, ammo_positions, ammo_sprites
    run = True
    game_over = False
    velocity_y = 0  # Vertical velocity of the player
    velocity_x = 0  # Horizontal velocity of the player
    recoil_force = 20  # Initial force applied on recoil
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if restart_rect.collidepoint((mx, my)):
                        ammo_count = 3
                        ammo_positions, ammo_sprites = spawn_ammo()
                        player_rect.center = (screenWidth // 2, screenHeight // 2)
                        velocity_x, velocity_y = 0, 0
                        game_over = False
                    elif exit_rect.collidepoint((mx, my)):
                        run = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and ammo_count > 0:
                    ammo_count -= 1
                    mx, my = pygame.mouse.get_pos()
                    angle = math.atan2(my - player_rect.centery, mx - player_rect.centerx)
                    velocity_x = -math.cos(angle) * recoil_force  # Apply the recoil force in the x direction
                    velocity_y = -math.sin(angle) * recoil_force  # Apply the recoil force in the y direction

        if not game_over:
            velocity_y += gravity  # Apply gravity
            player_rect.x += velocity_x  # Update player position based on horizontal velocity
            player_rect.y += velocity_y  # Update player position based on vertical velocity

            # Check if player falls through the ground
            if player_rect.top > screenHeight:
                game_over = True

            # Keep player within screen bounds (only x direction)
            if player_rect.left < 0:
                player_rect.right = screenWidth
            if player_rect.right > screenWidth:
                player_rect.left = 0

            # Check for ammo pickup
            for ammo_rect in ammo_positions:
                if player_rect.colliderect(ammo_rect):
                    ammo_positions.remove(ammo_rect)
                    ammo_count += 1

            # Respawn ammo if all are picked up
            if len(ammo_positions) == 0:
                ammo_positions, ammo_sprites = spawn_ammo()

        screen.fill((255, 253, 208))
        draw_ammo_count()
        screen.blit(player, player_rect.topleft)

        # Rotate the gun to point towards the mouse cursor
        mx, my = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(my - player_rect.centery, mx - player_rect.centerx))
        rotated_gun = pygame.transform.rotate(gun, -angle)

        # Position the gun relative to the player
        gun_offset_x = player_rect.width // 2
        gun_offset_y = player_rect.height // 3  # Adjust this value to fit the gun to the duck's body
        gun_pos = (player_rect.centerx + gun_offset_x * math.cos(math.radians(angle)),
                   player_rect.centery + gun_offset_y * math.sin(math.radians(angle)))
        gun_rect = rotated_gun.get_rect(center=gun_pos)
        screen.blit(rotated_gun, gun_rect.topleft)

        # Draw ammo on screen
        for ammo_rect, ammo_sprite in zip(ammo_positions, ammo_sprites):
            screen.blit(ammo_sprite, ammo_rect.topleft)

        if game_over:
            draw_game_over()
            restart_rect, exit_rect = draw_buttons()

        pygame.display.update()

        clock.tick(60)

def main_loop():
    global main, click
    while main:
        drawMainMenu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        pygame.display.update()

    game()
    pygame.quit()

main_loop()
