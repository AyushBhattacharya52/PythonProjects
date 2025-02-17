import pygame
from random import randint
pygame.init()

screenWidth = 1280
screenHeight = 720

screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption('Coffee Chaos')

bird_x = 50
bird_y = screenHeight // 2 - 75
gravity = 0.5
jump_strength = -10
velocity_y = 0
score = 0
speed_increment = 1

# Load and scale the bird image
bird = pygame.image.load(r'C:\\Users\\debra\\.vscode\\BirdHop\\Coffee Sprite.png').convert_alpha()
bird = pygame.transform.scale(bird, (bird.get_width() * 3, bird.get_height() * 3))
bird_r = bird.get_rect(center=(bird_x, bird_y))
bird_facing_right = True

# Load the coffee bean image
coffee_bean = pygame.image.load(r"C:\\Users\\debra\\.vscode\\BirdHop\\Coffee Bean Image.png").convert_alpha()
coffee_bean = pygame.transform.scale(coffee_bean, (int(coffee_bean.get_width() * 2.5), int(coffee_bean.get_height() * 2.5)))

clock = pygame.time.Clock()

def main():
    global speed_increment
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    speed_increment = 1
                    game()
                elif event.key == pygame.K_2:
                    speed_increment = 4
                    game()
                elif event.key == pygame.K_3:
                    speed_increment = 10
                    game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        screen.fill((255, 253, 208))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Press 1 for Normal, 2 for Speed, 3 for Lightning', True, (0, 0, 0))
        text_r = text.get_rect(center=(screenWidth // 2, screenHeight // 2))
        screen.blit(text, text_r)
        pygame.display.update()

def game():
    global bird_x, bird_y, gravity, jump_strength, speed, velocity_y, bird, bird_r, bird_facing_right
    global score, speed_increment
    bird_x = 50
    bird_y = screenHeight // 2 - 75
    velocity_y = 0
    score = 0
    speed = 5
    gravity = 0.5
    bird_r = bird.get_rect(center=(bird_x, bird_y))

    # Spawn a random number of coffee beans
    coffee_beans = spawn_coffee_beans()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity_y = jump_strength
        
        screen.fill((255, 253, 208))
        
        # Apply gravity
        velocity_y += gravity
        bird_y += velocity_y
        bird_r.y = bird_y

        # Apply horizontal movement
        bird_x += speed
        bird_r.x = bird_x

        # Bounce the bird off the screen edge
        if bird_r.left <= 0 or bird_r.right >= screenWidth:
            speed = -speed
            bird_facing_right = not bird_facing_right
            bird = pygame.transform.flip(bird, True, False)

        # Prevent the bird from falling below the screen
        if bird_r.bottom >= screenHeight:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Game Over!', True, (0, 0, 0))
            score_text = font.render(f'Score: {score}', True, (0, 0, 0))
            restart = font.render('Press w to restart', True, (0, 0, 0))
            screen.blit(text, (screenWidth // 2 - text.get_width() // 2, screenHeight // 2 - 25))
            screen.blit(score_text, (screenWidth // 2 - 50, screenHeight // 2 + 30))
            screen.blit(restart, (screenWidth // 2 - 100, screenHeight // 2 + 60))
            pygame.display.update()
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            waiting_for_restart = False
                            game()
                            return
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return

        # Draw the coffee beans
        for bean_r in coffee_beans:
            screen.blit(coffee_bean, bean_r)

        # Check for collision with coffee beans
        for bean_r in coffee_beans[:]:
            if bird_r.colliderect(bean_r):
                coffee_beans.remove(bean_r)
                if randint(0,500) <= 500:  # 50% chance for normal or poisoned effect
                    score += 1
                    speed += speed_increment
                else:
                    gravity += 0.5
                    speed -= 10

        # Respawn coffee beans if all are collected
        if not coffee_beans:
            coffee_beans = spawn_coffee_beans()

        screen.blit(bird, (bird_r.x, bird_r.y))
        pygame.display.update()
        clock.tick(60)

def spawn_coffee_beans():
    coffee_beans = []
    for _ in range(randint(1, 20)):
        bean_x = randint(100, screenWidth - 100)
        bean_y = randint(100, screenHeight - 100)
        coffee_beans.append(coffee_bean.get_rect(center=(bean_x, bean_y)))
    return coffee_beans

main()
