# main.py
import pygame
import sys
from level0 import run_level0
from level1 import run_level1
from level2 import run_level2

# Initialize Pygame
pygame.init()

# Window settings
MENU_WIDTH, MENU_HEIGHT = 800, 600
screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
pygame.display.set_caption("Шлях від НАУ до КАІ")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (86, 83, 131)
WHITE_BLUE = (111, 136, 204)
GRAY = (150, 150, 150)
TITLE_BG_COLOR = (56, 56, 56)

title_font = pygame.font.Font("style/Pixel_Font-7.ttf", 48)  # Larger font for title
button_font = pygame.font.Font("style/Pixel_Font-7.ttf", 20)

# Background and lock icon
background = pygame.image.load("menu_bg.png")
background = pygame.transform.scale(background, (MENU_WIDTH, MENU_HEIGHT))
lock_icon = pygame.image.load("lock.png")
lock_icon = pygame.transform.scale(lock_icon, (50, 50))  # Adjust size as needed

# Game state
level0_completed = False
level1_completed = False

def draw_button(text, x, y, width, height, inactive_color, active_color, enabled=True):
    button_text = button_font.render(text, True, WHITE)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)
    if enabled:
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, active_color, button_rect, border_radius=20)
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(screen, inactive_color, button_rect, border_radius=20)
    else:
        pygame.draw.rect(screen, GRAY, button_rect, border_radius=20)
        lock_rect = lock_icon.get_rect(center=button_rect.center)
        screen.blit(lock_icon, lock_rect)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    return False

def main_menu():
    global level0_completed, level1_completed
    running = True

    # Button dimensions and spacing
    button_width = 200
    button_height = 100
    spacing = 50
    total_width = (button_width * 3) + (spacing * 2)
    start_x = (MENU_WIDTH - total_width) // 2
    button_y = MENU_HEIGHT // 2 - button_height // 2

    while running:
        screen.blit(background, (0, 0))
        title_text = title_font.render("ШЛЯХ ВІД НАУ ДО КАІ", True, WHITE)
        title_rect = title_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 4))
        title_bg_rect = title_rect.inflate(20, 10)
        pygame.draw.rect(screen, TITLE_BG_COLOR, title_bg_rect, border_radius=10)
        screen.blit(title_text, title_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Stage 0
        if draw_button("Пара з історії", start_x, button_y, button_width, button_height, DARK_BLUE, WHITE_BLUE):
            pygame.display.set_mode((800, 600))
            if run_level0():
                level0_completed = True
            pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))

        # Stage 1
        if draw_button("Знайти Луцького", start_x + button_width + spacing, button_y, button_width, button_height, DARK_BLUE, WHITE_BLUE, enabled=level0_completed):
            pygame.display.set_mode((400, 700))
            if run_level1():
                level1_completed = True
            pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))

        # Stage 2
        if draw_button("Битва з Босом", start_x + (button_width + spacing) * 2, button_y, button_width, button_height, DARK_BLUE, WHITE_BLUE, enabled=level1_completed):
            pygame.display.set_mode((800, 600))
            run_level2()
            pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))

        # Exit button (below the row)
        exit_btn_y = button_y + button_height + 50
        if draw_button("Вихід", MENU_WIDTH // 2 - (button_font.render("Вихід", True, WHITE).get_width() + 40), exit_btn_y, 200, 100, DARK_BLUE, WHITE_BLUE):
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()