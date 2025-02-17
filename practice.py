import pygame
import sys
import math
# Initialize pygame
pygame.init()

# Set up display
width, height = 1000, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Calculator")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)

# Fonts
font = pygame.font.SysFont(None, 40)

# Calculator variables
input_text = ""
result = ""

# Button layout (number and operator positions)
buttons = [
    ('7', 50, 150), ('8', 150, 150), ('9', 250, 150), ('/', 350, 150),
    ('4', 50, 250), ('5', 150, 250), ('6', 250, 250), ('*', 350, 250),
    ('1', 50, 350), ('2', 150, 350), ('3', 250, 350), ('-', 350, 350),
    ('C', 50, 450), ('0', 150, 450), ('=', 250, 450), ('+', 350, 450)
]

# Button size
button_width, button_height = 80, 80

# Helper function to draw buttons
def draw_button(text, x, y, color=GRAY):
    pygame.draw.rect(window, color, (x, y, button_width, button_height))
    label = font.render(text, True, BLACK)
    window.blit(label, (x + (button_width - label.get_width()) / 2, y + (button_height - label.get_height()) / 2))

# Main loop
run = True
while run:
    window.fill(WHITE)
    
    # Display input and result text
    input_label = font.render(input_text, True, BLACK)
    result_label = font.render(result, True, BLUE)
    window.blit(input_label, (10, 20))
    window.blit(result_label, (10, 70))

    # Draw buttons
    for (text, x, y) in buttons:
        draw_button(text, x, y)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for (text, x, y) in buttons:
                if x < mx < x + button_width and y < my < y + button_height:
                    if text == 'C':
                        input_text = ""
                        result = ""
                    elif text == '=':
                        try:
                            result = str(eval(input_text))
                        except Exception as e:
                            result = "Error"
                    else:
                        input_text += text

    pygame.display.flip()

pygame.quit()
sys.exit()
