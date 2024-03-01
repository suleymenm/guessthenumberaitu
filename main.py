import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Aphex Twin - Flim.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Угадай число")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

input_text = ""
input_rect = pygame.Rect(20, 60, 200, 36)

guess_message = ""
max_attempts = 0
attempts = 0

music_on = True
music_button_rect = pygame.Rect(600, 20, 83, 50)
music_text = font.render("Выкл.", True, BLACK)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def toggle_music():
    global music_on
    if music_on:
        pygame.mixer.music.pause()
        music_on = False
    else:
        pygame.mixer.music.unpause()
        music_on = True

def show_difficulty_dialog():
    global max_attempts
    easy_button_rect = pygame.Rect(100, 200, 200, 50)
    medium_button_rect = pygame.Rect(100, 300, 200, 50)
    hard_button_rect = pygame.Rect(100, 400, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button_rect.collidepoint(event.pos):
                    difficulty_level("easy")
                    max_attempts = 10
                    return
                elif medium_button_rect.collidepoint(event.pos):
                    difficulty_level("medium")
                    max_attempts = 5
                    return
                elif hard_button_rect.collidepoint(event.pos):
                    difficulty_level("hard")
                    max_attempts = 3
                    return

        window.fill(WHITE)
        draw_text("Выберите уровень сложности:", font, BLACK, window, 20, 20)
        pygame.draw.rect(window, BLACK, easy_button_rect, 2)
        draw_text("Легкий", font, BLACK, window, easy_button_rect.x + 10, easy_button_rect.y + 10)
        pygame.draw.rect(window, BLACK, medium_button_rect, 2)
        draw_text("Средний", font, BLACK, window, medium_button_rect.x + 10, medium_button_rect.y + 10)
        pygame.draw.rect(window, BLACK, hard_button_rect, 2)
        draw_text("Сложный", font, BLACK, window, hard_button_rect.x + 10, hard_button_rect.y + 10)

        pygame.display.flip()

def difficulty_level(level):
    global number_to_guess
    if level == "easy":
        number_to_guess = random.randint(1, 100)
    elif level == "medium":
        number_to_guess = random.randint(1, 100)
    elif level == "hard":
        number_to_guess = random.randint(1, 100)

show_difficulty_dialog()

running = True
while running:
    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN and attempts < max_attempts:
                attempts += 1
                try:
                    guess = int(input_text)
                    if guess < number_to_guess:
                        guess_message = "Загаданное число больше."
                    elif guess > number_to_guess:
                        guess_message = "Загаданное число меньше."
                    else:
                        guess_message = "Поздравляем! Вы угадали число."
                        running = True
                except ValueError:
                    guess_message = "Пожалуйста, введите целое число."
                input_text = ""
                if attempts == max_attempts:
                    guess_message += " Попытки закончились."
                    running = True
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if music_button_rect.collidepoint(event.pos):
                toggle_music()

    draw_text("Угадайте число. Попыток осталось: " + str(max_attempts - attempts), font, BLACK, window, 20, 20)
    draw_text(guess_message, font, BLACK, window, 20, 100)
    pygame.draw.rect(window, BLACK, input_rect, 2)
    draw_text(input_text, font, BLACK, window, input_rect.x + 5, input_rect.y + 5)

    pygame.draw.rect(window, BLACK, music_button_rect, 2)
    window.blit(music_text, (music_button_rect.x + 10, music_button_rect.y + 10))

    pygame.display.flip()

pygame.quit()
