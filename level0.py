# level0.py
import pygame
import time

# Initialize Pygame (moved to run_level0 for multi-stage compatibility)
def run_level0():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stage 0: Quiz")

    background = pygame.image.load("img/screen.png")

    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    GREEN = (0, 255, 0)
    DARK_RED = (255, 0, 0)
    DARK_BLUE = (86, 83, 131)
    WHITE_BLUE = (111, 136, 204)

    click_areas = [
        pygame.Rect(500, 100, 100, 100),
        pygame.Rect(610, 100, 100, 100),
        pygame.Rect(500, 210, 100, 100),
        pygame.Rect(610, 210, 100, 100),
        pygame.Rect(500, 320, 100, 100),
        pygame.Rect(610, 320, 100, 100)
    ]

    questions = [
        ("Чи виступав Луцький у партії регіонів?", "Так"),
        ("Чи була у Луцького баня в 1 корпусі?", "Так"),
        ("Чи правда, що 3 курс називають 'мінусамі'?", "Ні"),
        ("Правда, що в 8 корпусі була найсмачніша піцца?", "Так"),
        ("Якщо йдеш в університет 'КАІ', ти вже поїхав головою?", "Так"),
        ("Чи правда, що в 'КАІ' закуповують на пів мільйона гривень туалетного паперу?", "Так")
    ]

    question_rect = pygame.Rect(150, 100, 500, 250)
    yes_button = pygame.Rect(250, 370, 120, 60)
    no_button = pygame.Rect(430, 370, 120, 60)
    feedback_rect = pygame.Rect(150, 20, 500, 80)

    font = pygame.font.Font(None, 42)
    small_font = pygame.font.Font(None, 36)

    def draw_button(text, x, y, inactive_color, active_color):
        button_text = small_font.render(text, True, WHITE)
        padding_x, padding_y = 20, 10
        width = button_text.get_width() + padding_x * 2
        height = button_text.get_height() + padding_y * 2
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_rect = pygame.Rect(x, y, width, height)
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, active_color, (x, y, width, height), border_radius=20)
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(screen, inactive_color, (x, y, width, height), border_radius=20)
        text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(button_text, text_rect)
        return False

    def show_thank_you_screen():
        screen.fill(WHITE)
        thank_you_text = pygame.font.Font(None, 50).render("Дякую за увагу, тим хто слухав!", True, BLACK)
        screen.blit(thank_you_text, (WIDTH // 2 - thank_you_text.get_width() // 2, HEIGHT // 2 - 100))
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            if draw_button("Continue", WIDTH // 2 - (small_font.render("Continue", True, WHITE).get_width() + 40) // 2, HEIGHT // 2, DARK_BLUE, WHITE_BLUE):
                waiting = False
            pygame.display.flip()
        return True

    show_question = False
    current_question = ""
    correct_answer = ""
    user_answer = ""
    feedback_text = ""
    selected_index = None

    running = True
    while running:
        screen.blit(background, (0, 0))

        if all(rect is None for rect in click_areas):
            if show_thank_you_screen():
                running = False  # Exit cleanly on completion
            else:
                return False  # Quit during thank you screen
            break

        for i, rect in enumerate(click_areas):
            if rect:
                pygame.draw.rect(screen, RED, rect, 3)
                pygame.draw.rect(screen, WHITE, rect.inflate(-6, -6))
                text_surface = font.render(str(i + 1), True, BLACK)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

        if feedback_text:
            pygame.draw.rect(screen, WHITE, feedback_rect, border_radius=10)
            feedback_surface = small_font.render(feedback_text, True, BLACK)
            screen.blit(feedback_surface, feedback_surface.get_rect(center=feedback_rect.center))

        if show_question:
            pygame.draw.rect(screen, GRAY, question_rect, border_radius=15)
            pygame.draw.rect(screen, GREEN, yes_button, border_radius=10)
            pygame.draw.rect(screen, DARK_RED, no_button, border_radius=10)

            words = current_question.split()
            lines = []
            while words:
                line = ''
                while words and font.size(line + words[0])[0] < question_rect.width - 40:
                    line += (words.pop(0) + ' ')
                lines.append(line)

            y_offset = question_rect.y + 30
            for line in lines:
                text_surface = small_font.render(line, True, BLACK)
                screen.blit(text_surface, (question_rect.x + 20, y_offset))
                y_offset += 40

            yes_text = small_font.render("Так", True, BLACK)
            no_text = small_font.render("Ні", True, BLACK)
            screen.blit(yes_text, (yes_button.x + 40, yes_button.y + 15))
            screen.blit(no_text, (no_button.x + 40, no_button.y + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_question:
                    if yes_button.collidepoint(event.pos):
                        user_answer = "Так"
                    elif no_button.collidepoint(event.pos):
                        user_answer = "Ні"
                    feedback_text = "Правильно!" if user_answer == correct_answer else "Неправильно!"
                    if user_answer == correct_answer and selected_index is not None:
                        click_areas[selected_index] = None
                    show_question = False
                else:
                    for i, rect in enumerate(click_areas):
                        if rect and rect.collidepoint(event.pos):
                            current_question, correct_answer = questions[i]
                            user_answer = ""
                            feedback_text = ""
                            show_question = True
                            selected_index = i

        pygame.display.flip()

    return all(rect is None for rect in click_areas)  # True if all questions answered correctly

if __name__ == "__main__":
    run_level0()
    pygame.quit()