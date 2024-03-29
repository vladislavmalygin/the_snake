from random import randint, choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка - Нажмите + или - для изменения скорости')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    GameObject — это базовый класс, от которого наследуются другие объекты.
    Он содержит общие атрибуты игровых объектов —
    например, эти атрибуты описывают позицию и цвет объекта.
    Этот же класс содержит и заготовку метода для отрисовки объекта
    на игровом поле — draw.
    """

    def __init__(self, body_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Заготовка для метода отрисовывающего класс"""
        raise NotImplementedError('Метод draw переопределен в дочернем классе')


class Apple(GameObject):
    """Класс Apple представляет яблоко, которое может быть съедено змеей."""

    def __init__(self, occupied_cells=()):
        """Инициализирует объект яблока с начальными параметрами."""
        super().__init__(APPLE_COLOR)
        self.position = None
        self.randomize_position(occupied_cells)
        self.last = None

    def randomize_position(self, occupied_cells):
        """Устанавливает случайную позицию для яблока на игровом поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake представляет змею, которой управляет игрок в игре."""

    def __init__(self):
        """Инициализирует объект змеи с начальными параметрами."""
        super().__init__(SNAKE_COLOR)
        self.last = None
        self.reset()
        self.direction = RIGHT
        self.next_direction = None

    def move(self):
        """Перемещает змею на один шаг в заданном направлении."""
        differ_x, differ_y = self.direction
        head_x, head_y = self.get_head_position()
        new_head = ((head_x + differ_x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + differ_y * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()
        else:
            self.last = None

    # Метод draw класса Snake
    def draw(self):
        """Отрисовывает змею на экране."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last[0], (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(snake, events):
    """Функция обрабатывающая ввод с клавиатуры"""
    global SPEED
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pg.K_EQUALS:  # Клавиша "+"
                SPEED += 1
            elif event.key == pg.K_MINUS:  # Клавиша "-"
                SPEED -= 1


def main():
    """Основная функция содержащая игровую логику"""
    # Инициализация PyGame:
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                handle_keys(snake, [event])

        snake.move()

        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
