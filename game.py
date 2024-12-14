import pygame
import random
import sys

# Список слов
words = [
    "яблоко", "машина", "компьютер", "книга", "дом", "школа", "спорт", "музыка", "кино",
    "солнце", "луна", "звезда", "река", "гора", "лес", "море", "океан", "птица", "рыба",
    "цветок", "дерево", "трава", "ветер", "дождь", "снег", "праздник", "путешествие", "друзья",
    "семья", "любовь", "счастье", "работа", "учеба", "игра", "фильм", "сказка", "музыка", "танец",
    "картинка", "фотография", "видео", "песня", "свет", "тень", "вода", "огонь", "земля", "воздух"
]

# Инициализация Pygame
pygame.init()

# Размеры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
button_color = (0, 255, 0)  # Цвет кнопки

# Шрифт
font = pygame.font.SysFont("Arial", 30)

# Таймер
clock = pygame.time.Clock()

# Время для ввода слова
time_limit = 10  # секунд

# Используемое множество для хранения использованных слов
used_words = set()

# Функция для получения нового слова
def get_new_word():
    available_words = list(set(words) - used_words)
    if available_words:
        new_word = random.choice(available_words)
        used_words.add(new_word)
        return new_word
    return None

# Функция для сброса игры
def reset_game():
    global current_word, start_time, input_word, current_attempt, circle_radius, lost, game_over, used_words
    used_words = set()
    current_word = get_new_word()
    start_time = pygame.time.get_ticks()
    input_word = ""
    current_attempt = 0
    circle_radius = initial_circle_radius
    lost = False
    game_over = False

def draw_button(text, x, y, width, height):
    button_color = white  # Устанавливаем белый цвет для кнопок
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    text_surface = font.render(text, True, black)  # Текст будет чёрным для контраста
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


# Функция для отображения меню
def main_menu():
    while True:
        screen.fill(black)
        draw_button("Играть", screen_width // 2 - 75, screen_height // 2 - 100, 150, 50)
        draw_button("Настройки", screen_width // 2 - 75, screen_height // 2, 150, 50)
        draw_button("Выход", screen_width // 2 - 75, screen_height // 2 + 100, 150, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if screen_width // 2 - 75 < mouse_x < screen_width // 2 + 75:
                    if screen_height // 2 - 100 < mouse_y < screen_height // 2 - 50:
                        return  # Начать игру
                    elif screen_height // 2 < mouse_y < screen_height // 2 + 50:
                        settings_menu()
                    elif screen_height // 2 + 100 < mouse_y < screen_height // 2 + 150:
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Функция для отображения настроек
def settings_menu():
    while True:
        screen.fill(black)
        draw_button("Назад", screen_width // 2 - 75, screen_height - 100, 150, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if screen_width // 2 - 75 < mouse_x < screen_width // 2 + 75 and screen_height - 100 < mouse_y < screen_height - 50:
                    return  # Вернуться в меню

        pygame.display.flip()
        clock.tick(60)

# Запуск главного меню
main_menu()

# Текущее слово
current_word = get_new_word()

# Время начала таймера
start_time = pygame.time.get_ticks()

# Начальный размер круга
initial_circle_radius = 100
circle_radius = initial_circle_radius

# Позиция круга
circle_x = screen_width // 2
circle_y = screen_height // 2

# Вводимое слово
input_word = ""

# Переменные для отслеживания результатов
best_attempt = 0
current_attempt = 0

# Флаги для окончания игры
game_over = False
lost = False  # Флаг для проигрыша

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.unicode == '\r' and not game_over and not lost:  # Проверка нажатия Enter
                if input_word == current_word:
                    current_attempt += 1
                    current_word = get_new_word()
                    start_time = pygame.time.get_ticks()
                    input_word = ""
                    circle_radius = initial_circle_radius  # Сброс радиуса круга
                    circle_x = screen_width // 2  # Сброс позиции круга
                    circle_y = screen_height // 2
                else:
                    input_word = ""
            elif event.key == pygame.K_BACKSPACE:  # Проверка нажатия Backspace
                input_word = input_word[:-1]  # Удаление последней буквы
            elif event.key == pygame.K_F11:  # Переключение полноэкранного режима
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((screen_width, screen_height))  # Окно
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Полноэкранный режим
                # Обновление координат круга для центрирования
                screen_width, screen_height = screen.get_size()
                circle_x = screen_width // 2
                circle_y = screen_height // 2
            else:
                input_word += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Проверка нажатия кнопки мыши
            mouse_x, mouse_y = event.pos
            if lost and (screen_width // 2 - 75 < mouse_x < screen_width // 2 + 75) and (screen_height // 2 + 50 < mouse_y < screen_height // 2 + 100):
                reset_game()  # Сброс игры при нажатии на кнопку

    # Время, прошедшее с начала таймера
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

    # Отрисовка экрана
    screen.fill(black)

    # Отрисовка текущего слова
    if not game_over and not lost:
        text_surface = font.render(current_word, True, white)
        text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(text_surface, text_rect)

        # Отрисовка введенного слова
        input_surface = font.render(input_word, True, white)
        input_rect = input_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        screen.blit(input_surface, input_rect)

        # Отрисовка лучшей попытки
        best_attempt = max(best_attempt, current_attempt)
        best_surface = font.render(f"Лучшая попытка: {best_attempt}", True, white)
        best_rect = best_surface.get_rect(center=(screen_width / 2, screen_height - 50))
        screen.blit(best_surface, best_rect)

        # Уменьшение радиуса круга в зависимости от времени
        if elapsed_time < time_limit:
            circle_radius = initial_circle_radius * (1 - (elapsed_time / time_limit))  # Уменьшение радиуса

        # Отрисовка круга, если он еще видим
        if circle_radius > 0:
            pygame.draw.circle(screen, white, (circle_x, circle_y), int(circle_radius), 10)  # Ширина 10

        # Проверка таймера
        if elapsed_time >= time_limit:
            lost = True  # Устанавливаем флаг проигрыша
            current_attempt = 0  # Сброс текущей попытки
            current_word = get_new_word()  # Получить новое слово
            start_time = pygame.time.get_ticks()  # Сброс таймера
            input_word = ""  # Сброс ввода
            circle_radius = initial_circle_radius  # Сброс радиуса круга
            circle_x = screen_width // 2  # Сброс позиции круга
            circle_y = screen_height // 2

        # Проверка окончания игры только после успешного ввода слова
        if current_word is None and not game_over:
            game_over = True

    # Отображение сообщения о проигрыше
    if lost:
        lost_surface = font.render("Вы проиграли, не успели", True, white)
        lost_rect = lost_surface.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(lost_surface, lost_rect)

        # Отображение кнопки "Возродиться"
        draw_button("Возродиться", screen_width // 2 - 75, screen_height // 2 + 50, 150, 50)

    # Отображение сообщения о победе
    if game_over:
        victory_surface = font.render("Победа! Вы написали все слова", True, white)
        victory_rect = victory_surface.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(victory_surface, victory_rect)

    # Обновление экрана
    pygame.display.flip()

    # Ограничение скорости
    clock.tick(60)