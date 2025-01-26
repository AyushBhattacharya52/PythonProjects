import pygame
import sys
import time

pygame.init()
clock = pygame.time.Clock()

screenWidth = 1280
screenHeight = 720
ground_y = screenHeight - 195

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('2 Player Fighting Game')

# Player positions and velocities
player1_x = 100
player1_y = ground_y
player1_velocity_y = 0
player1_speed = 5
player1_on_ground = True
player1_health = 100
player1_facing = 'right'
player1_last_shot_time = 0
player1_special_shot_time = -5
player1_e_count = 1

player2_x = 1100
player2_y = ground_y
player2_velocity_y = 0
player2_speed = 5
player2_on_ground = True
player2_health = 100
player2_facing = 'left'
player2_last_shot_time = 0
player2_special_shot_time = -5

# Gravity and jump constants
gravity = 0.1
jump_strength = -10

player_1 = pygame.Rect(player1_x, player1_y, 50, 50)
player_2 = pygame.Rect(player2_x, player2_y, 50, 50)

bullets = []
bullet_cooldown = 0.4  # Cooldown period in seconds

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 50)
text = font.render('2 Player Fighting Game', True, (0, 0, 0))
button_font = pygame.font.Font('freesansbold.ttf', 40)
button_text = button_font.render('Start Game', True, (255, 255, 255))
end_font = pygame.font.Font('freesansbold.ttf', 80)

click = False

# Load background image with error handling
try:
    bg = pygame.image.load(r'C:\Users\debra\.vscode\2 player fighting game\game_bg.png').convert()
    bg = pygame.transform.scale(bg, (screenWidth, screenHeight))  # Scale the background image to fit the screen
except pygame.error as e:
    print(f"Unable to load image: {e}")
    pygame.quit()
    sys.exit()

try:
    bg2 = pygame.image.load(r'C:\Users\debra\.vscode\2 player fighting game\game_bg_gameStart.jpg').convert()
    bg2 = pygame.transform.scale(bg2, (screenWidth, screenHeight))  # Scale the background image to fit the screen
except pygame.error as e:
    print(f"Unable to load image: {e}")
    pygame.quit()
    sys.exit()

def draw_button(screen, text, rect_color, x, y, width, height):
    pygame.draw.rect(screen, rect_color, (x, y, width, height))
    screen.blit(text, (x + (width - text.get_width()) // 2, y + (height - text.get_height()) // 2))

def mainMenu():
    global click
    run = True
    while run:
        screen.blit(bg, (0, 0))
        screen.blit(text, (screenWidth // 2 - text.get_width() // 2, screenHeight // 10))
        
        mx, my = pygame.mouse.get_pos()
        button_rect = pygame.Rect(screenWidth // 2 - 140, screenHeight // 2, 300, 100)

        if button_rect.collidepoint((mx, my)):
            if click:
                game()
        draw_button(screen, button_text, (0, 0, 255), button_rect.x, button_rect.y, button_rect.width, button_rect.height)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)  # Cap the frame rate to 60 FPS

    pygame.quit()
    sys.exit()

def game():
    global player1_x, player1_y, player1_velocity_y, player1_on_ground, player1_health, player1_facing, player1_last_shot_time, player1_special_shot_time, player1_e_count
    global player2_x, player2_y, player2_velocity_y, player2_on_ground, player2_health, player2_facing, player2_last_shot_time, player2_special_shot_time

    game_running = True
    while game_running:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        keys = pygame.key.get_pressed()

        # Player 1 controls (WASD)
        if keys[pygame.K_a] and player1_x > 0:
            player1_x -= player1_speed
            player1_facing = 'left'
        if keys[pygame.K_d] and player1_x < screenWidth:
            player1_x += player1_speed
            player1_facing = 'right'
        if keys[pygame.K_w] and player1_on_ground:
            player1_velocity_y = jump_strength
            player1_on_ground = False
        if keys[pygame.K_q] and current_time - player1_last_shot_time > bullet_cooldown:
            direction = player1_facing
            bullets.append({'x': player1_x + 25, 'y': player1_y + 25, 'direction': direction, 'player': 1})
            player1_last_shot_time = current_time
        if keys[pygame.K_s] and not player1_on_ground:
            if current_time - player1_last_shot_time > bullet_cooldown:
                direction = 'down'  # Indicate shooting downwards
                bullets.append({'x': player1_x + 25, 'y': player1_y + 25, 'direction': direction, 'player': 1})
                player1_last_shot_time = current_time
        if keys[pygame.K_e] and player1_e_count <= 3:
            if current_time - player1_last_shot_time > bullet_cooldown:
                direction = player1_facing
                player1_health += 30
                player1_e_count += 1
                player1_special_shot_time = current_time
        if keys[pygame.K_r]:
            if current_time - player1_special_shot_time > bullet_cooldown:
                direction = "fastleft"
                bullets.append({'x': player1_x + 25, 'y': player1_y + 25, 'direction': direction, 'player': 1})       
                direction = "fastright"
                bullets.append({'x': player1_x + 25, 'y': player1_y + 25, 'direction': direction, 'player': 1})            
            player1_special_shot_time = current_time
        # Player 2 controls (Arrow keys)
        if keys[pygame.K_LEFT] and player2_x > 0:
            player2_x -= player2_speed
            player2_facing = 'left'
        if keys[pygame.K_RIGHT] and player2_x < screenWidth:
            player2_x += player2_speed
            player2_facing = 'right'
        if keys[pygame.K_UP] and player2_on_ground:
            player2_velocity_y = jump_strength
            player2_on_ground = False
        if keys[pygame.K_p] and current_time - player2_last_shot_time > bullet_cooldown:
            direction = player2_facing
            bullets.append({'x': player2_x + 25, 'y': player2_y + 25, 'direction': direction, 'player': 2})
            player2_last_shot_time = current_time
        if keys[pygame.K_DOWN] and not player2_on_ground:
            if current_time - player2_last_shot_time > bullet_cooldown:
                direction = 'down'  # Indicate shooting downwards
                bullets.append({'x': player2_x + 25, 'y': player2_y + 25, 'direction': direction, 'player': 2})
        if keys[pygame.K_1]:
            if current_time - player1_last_shot_time > bullet_cooldown:
                direction = 'up' # Indicate shooting
                bullets.append({'x': player1_x + 25, 'y': player1_y + 25, 'direction': direction, 'player': 1})
                direction = 'down' # Indicate shooting
                bullets.append({'x': player1_x + 25, 'y': player1_y + 25, 'direction': direction, 'player': 1})
                direction = 'right' # Indicate shooting
                bullets.append({'x': player1_x + 25, 'y': player1_y + 25, 'direction': direction, 'player': 1})
                direction = 'left' # Indicate shooting
                bullets.append({'x': player1_x + 25, 'y': player1_y + 25, 'direction': direction, 'player': 1})
                player1_last_shot_time = current_time
               
        # Apply gravity
        if not player1_on_ground:
            player1_velocity_y += gravity
        if not player2_on_ground:
            player2_velocity_y += gravity

        # Update player positions
        player1_y += player1_velocity_y
        player2_y += player2_velocity_y

        # Check if players are on the ground
        if player1_y >= ground_y:
            player1_y = ground_y
            player1_velocity_y = 0
            player1_on_ground = True

        if player2_y >= ground_y:
            player2_y = ground_y
            player2_velocity_y = 0
            player2_on_ground = True

        # Update bullets
        for bullet in bullets[:]:
            if bullet['direction'] == 'right':
                bullet['x'] += 10
            elif bullet['direction'] == 'down':
                bullet['y'] += 10
            elif direction == "up":
                bullet['y'] -= 10
            elif direction == "fastleft":
                bullet['x'] -= 50
            elif direction == "fastright":
                bullet['x'] += 50
            else:
                bullet['x'] -= 10
            
            # Check collision with player 1
            if bullet['player'] == 2 and player1_x < bullet['x'] < player1_x + 50 and player1_y < bullet['y'] < player1_y + 50:
                player1_health -= 10
                bullets.remove(bullet)
            
            # Check collision with player 2
            elif bullet['player'] == 1 and player2_x < bullet['x'] < player2_x + 50 and player2_y < bullet['y'] < player2_y + 50:
                player2_health -= 10
                bullets.remove(bullet)
            elif bullet['player'] == 1 and player2_x < bullet['x'] < player2_x + 50 and player2_y < bullet['y'] < player2_y + 50 and bullet[bullet['direction'] == 'fastright':]:
                player2_health -= 60
                bullets.remove(bullet)
            
            # Remove bullets that go off-screen
            if bullet['x'] < 0 or bullet['x'] > screenWidth:
                bullets.remove(bullet)

        # Draw game elements
        screen.blit(bg2, (0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (player1_x, player1_y, 50, 50))  # Draw player 1
        pygame.draw.rect(screen, (0, 0, 255), (player2_x, player2_y, 50, 50))  # Draw player 2
        
        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, (0, 255, 0), (bullet['x'], bullet['y']), 5)
        
        # Draw health bars
        pygame.draw.rect(screen, (255, 0, 0), (50, 50, player1_health * 2, 25))  # Player 1 health bar
        pygame.draw.rect(screen, (0, 0, 255), (screenWidth - 250, 50, player2_health * 2, 25))  # Player 2 health bar

        # Check for game end conditions
        if player1_health <= 0:
            winner_text = end_font.render('Player 2 Wins!', True, (0, 0, 255))
            screen.blit(winner_text, (screenWidth // 2 - winner_text.get_width() // 2, screenHeight // 2 - winner_text.get_height() // 2))
            pygame.display.update()
            time.sleep(1)
            mainMenu()
        elif player2_health <= 0:
            winner_text = end_font.render('Player 1 Wins!', True, (255, 0, 0))
            screen.blit(winner_text, (screenWidth // 2 - winner_text.get_width() // 2, screenHeight // 2 - winner_text.get_height() // 2))
            pygame.display.update()
            time.sleep(1)
            mainMenu()

        pygame.display.update()
        clock.tick(60)  # Cap the frame rate to 60 FPS

    pygame.quit()
    sys.exit()

mainMenu()
