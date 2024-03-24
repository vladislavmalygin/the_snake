from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    GameObject — это базовый класс, от которого наследуются другие объекты.
    Он содержит общие атрибуты игровых объектов —
    например, эти атрибуты описывают позицию и цвет объекта.
    Этот же класс содержит и заготовку метода для отрисовки объекта
    на игровом поле — draw.
    """

    def __init__(self):
        self.position = None
        self.body_color = None

    def init(self, position=(0, 0)):
        """
        Инициализирует объект змеи с заданной позицией.

        Аргументы:
            position (кортеж): Начальная позиция змеи на игровом поле.
        """
        self.position = position
        self.body_color = None

    def draw(self):
        """Заготовка для метода отрисовывающего класс"""
        pass


class Apple(GameObject):
    """Класс Apple представляет яблоко, которое может быть съедено змеей."""

    def __init__(self):
        """Инициализирует объект яблока с начальными параметрами."""
        super().__init__()
        self.position = None
        self.body_color = (255, 0, 0)
        self.randomize_position()
        self.last = None

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока на игровом поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake представляет змею, которой управляет игрок в игре."""

    def __init__(self):
        """Инициализирует объект змеи с начальными параметрами."""
        super().__init__()
        self.last = None
        self.length = 1
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)

    def move(self):
        """Перемещает змею на один шаг в заданном направлении."""
        dx, dy = self.direction
        head_x, head_y = self.positions[0]
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    # Метод draw класса Snake
    def draw(self):
        """Отрисовывает змею на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление движения змеи на следующее направление."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает параметры змеи до начальных значений."""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None

    def eat_apple(self, apple):
        """Проверяет, съела ли змея яблоко."""
        head_rect = pygame.Rect(self.positions[0][0], self.positions[0][1],
                                GRID_SIZE, GRID_SIZE)
        apple_rect = pygame.Rect(apple.position[0], apple.position[1],
                                 GRID_SIZE, GRID_SIZE)
        return head_rect.colliderect(apple_rect)

    def self_collision(self):
        """Проверяет наличие столкновений сегментов тела змеи."""
        return len(self.positions) != len(set(self.positions))


def handle_keys(snake, events):
    """Функция обрабатывающая ввод с клавиатуры"""
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция содержащая игровую логику"""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                handle_keys(snake, [event])

        snake.update_direction()

        if snake.eat_apple(apple):
            snake.length += 1
            apple.randomize_position()

        snake.move()

        if snake.self_collision():
            snake.reset()

        screen.fill((0, 0, 0))
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
