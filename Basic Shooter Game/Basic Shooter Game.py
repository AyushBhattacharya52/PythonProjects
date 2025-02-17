import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Basic Shooter Game")

# Fonts
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# Initial circle properties
Shooter_center = [800 // 2, 600 // 2]  # Center of the screen, use list for mutable
Shooter_radius = 30
Shooter_color = (255, 0, 0)  # Red color
Bullet_color = (64, 64, 64)
Bullet_radius = 5
can_shoot = True
bullet_cooldown = 500  # Cooldown in milliseconds
last_shot_time = 0

# Movement speed
speed = 5

# Movement flags
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Bullet list
bullets = []

class Bullet:
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.speed = 10

    def update(self):
        self.pos[0] += self.speed * math.cos(self.angle)
        self.pos[1] += self.speed * math.sin(self.angle)

    def draw(self, screen):
        pygame.draw.circle(screen, Bullet_color, (int(self.pos[0]), int(self.pos[1])), Bullet_radius)

class Enemy:
    def __init__(self, pos, speed, color, health):
        self.pos = pos
        self.speed = speed
        self.color = color
        self.radius = 20
        self.health = health

    def update(self):
        dx = Shooter_center[0] - self.pos[0]
        dy = Shooter_center[1] - self.pos[1]
        angle = math.atan2(dy, dx)
        self.pos[0] += self.speed * math.cos(angle)
        self.pos[1] += self.speed * math.sin(angle)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

def spawn_enemy(wave):
    side = random.choice(["left", "right", "top", "bottom"])
    if side == "left":
        pos = [0, random.randint(0, 600)]
    elif side == "right":
        pos = [800, random.randint(0, 600)]
    elif side == "top":
        pos = [random.randint(0, 800), 0]
    else:
        pos = [random.randint(0, 800), 600]
    speed = wave["enemy_speed"]
    color = [random.randint(0, 255) for _ in range(3)]
    health = wave["enemy_health"]
    enemies.append(Enemy(pos, speed, color, health))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Enemy list
enemies = []

# Wave definitions
waves = [
    {"num_enemies": 5, "enemy_speed": 2, "enemy_health": 1},
    {"num_enemies": 10, "enemy_speed": 2.5, "enemy_health": 2},
    {"num_enemies": 15, "enemy_speed": 3, "enemy_health": 3},
    # Add more waves as needed
]

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2
game_state = START

# Score variables
score = 0
high_score = 0

# Current wave
current_wave = 0
enemies_spawned = 0

# Load high score from file
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    # If highscore.txt does not exist, start with high_score = 0
    high_score = 0

def initialize_wave(wave):
    global enemies_spawned
    enemies_spawned = 0
    for _ in range(wave["num_enemies"]):
        spawn_enemy(wave)

while True:
    screen.fill((0, 0, 0))  # Fill the screen with black

    if game_state == START:
        draw_text("Basic Shooter Game", font, (255, 255, 255), screen, 400, 200)
        draw_text("Press any key to start", small_font, (255, 255, 255), screen, 400, 300)
        
    elif game_state == PLAYING:
        pygame.draw.circle(screen, Shooter_color, Shooter_center, Shooter_radius)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Calculate direction from the center of the circle to the mouse position
        dx = mouse_pos[0] - Shooter_center[0]
        dy = mouse_pos[1] - Shooter_center[1]
        angle = math.atan2(dy, dx)

        # Calculate the end point of the line
        line_length = Shooter_radius + 20  # Length of the line extending out of the circle
        line_end_x = Shooter_center[0] + line_length * math.cos(angle)
        line_end_y = Shooter_center[1] + line_length * math.sin(angle)

        # Draw the line
        pygame.draw.line(screen, Shooter_color, Shooter_center, (line_end_x, line_end_y), 2)

        # Draw bullets
        for bullet in bullets:
            bullet.update()
            bullet.draw(screen)

        # Draw enemies
        for enemy in enemies:
            enemy.update()
            enemy.draw(screen)
            # Check collision with shooter
            if math.hypot(enemy.pos[0] - Shooter_center[0], enemy.pos[1] - Shooter_center[1]) < (Shooter_radius + enemy.radius):
                game_state = GAME_OVER

        # Check bullet collisions with enemies
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if math.hypot(bullet.pos[0] - enemy.pos[0], bullet.pos[1] - enemy.pos[1]) < (Bullet_radius + enemy.radius):
                    bullets.remove(bullet)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        score += 1
                        if score > high_score:
                            high_score = score
                    break

        # Check if wave is cleared
        if enemies_spawned >= waves[current_wave]["num_enemies"] and len(enemies) == 0:
            current_wave += 1
            if current_wave < len(waves):
                initialize_wave(waves[current_wave])
            else:
                # Game won scenario, reset game
                game_state = GAME_OVER

        # Spawn enemies at intervals
        current_time = pygame.time.get_ticks()
        if current_wave < len(waves) and enemies_spawned < waves[current_wave]["num_enemies"]:
            spawn_enemy(waves[current_wave])
            enemies_spawned += 1

        # Draw score, high score, and wave number
        draw_text(f'Score: {score}', small_font, (255, 255, 255), screen, 70, 30)
        draw_text(f'High Score: {high_score}', small_font, (255, 255, 255), screen, 700, 30)
        draw_text(f'Wave: {current_wave + 1}', small_font, (255, 255, 255), screen, 400, 30)

    elif game_state == GAME_OVER:
        draw_text("Game Over", font, (255, 255, 255), screen, 400, 200)
        draw_text(f'Score: {score}', small_font, (255, 255, 255), screen, 400, 300)
        draw_text(f'High Score: {high_score}', small_font, (255, 255, 255), screen, 400, 350)
        draw_text("Press any key to restart", small_font, (255, 255, 255), screen, 400, 400)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save high score to file before quitting
            with open("highscore.txt", "w") as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state == START or game_state == GAME_OVER:
                # Reset game variables
                Shooter_center = [800 // 2, 600 // 2]
                bullets = []
                enemies = []
                score = 0
                current_wave = 0
                initialize_wave(waves[current_wave])
                game_state = PLAYING
            if game_state == PLAYING:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    moving_up = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    moving_down = True
                if event.key == pygame.K_SPACE:
                    if can_shoot and current_time - last_shot_time >= bullet_cooldown:
                        bullet_pos = [line_end_x, line_end_y]
                        bullets.append(Bullet(bullet_pos, angle))
                        can_shoot = False
                        last_shot_time = current_time

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moving_down = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == PLAYING:
                if can_shoot and current_time - last_shot_time >= bullet_cooldown:
                    bullet_pos = [line_end_x, line_end_y]
                    bullets.append(Bullet(bullet_pos, angle))
                    can_shoot = False
                    last_shot_time = current_time

    if game_state == PLAYING:
        # Update circle position
        if moving_left:
            Shooter_center[0] -= speed
        if moving_right:
            Shooter_center[0] += speed
        if moving_up:
            Shooter_center[1] -= speed
        if moving_down:
            Shooter_center[1] += speed

        # Handle shooting cooldown
        if not can_shoot and current_time - last_shot_time >= bullet_cooldown:
            can_shoot = True

    clock.tick(60)
