from tkinter import *
import random

window = Tk()
window.title("Snake Game Python")
window.resizable(0, 0)

Label(window, text='Project_AI_M.Haris.Zaman_452133', font='arial 20 bold').pack(side=BOTTOM)

score = 0
direction = 'down'

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 180
SPACE_SIZE = 50
BODY_PARTS = 2
SNAKE_COLOR = 'red'
FOOD_COLOR = 'blue'
BACKGROUND_COLOR = 'green'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        self.coordinates = []
        self.square = None
        self.spawn_food()

    def spawn_food(self):
        while True:
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

            # Check if the food coordinates overlap with any obstacle
            overlap = any(
                obs_x <= x < obs_x + SPACE_SIZE and obs_y <= y < obs_y + SPACE_SIZE
                for obs_x, obs_y in obstacle.coordinates
            )

            if not overlap:
                break

        self.coordinates = [x, y]
        self.square = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag='food')


class Obstacle:
    def __init__(self):
        # Define coordinates for the swastika shape
        self.coordinates = [
            (400, 450),
            (400, 400),
            (700, 750),
            (750, 800),
            (350, 400),
            (300, 450),
            (300, 500),
            (300, 300),
            (900, 950),
            (950, 1000),
            (500, 500),
            (500, 350),
            (500, 300),
            (400, 500),
            (400, 300),
            (500, 400),
            (300, 400),
        ]

        # Create rectangles for each part of the swastika on the canvas
        for coord in self.coordinates:
            canvas.create_rectangle(coord[0], coord[1], coord[0] + SPACE_SIZE, coord[1] + SPACE_SIZE,
                                     fill='gray', tag='obstacle')


class PCSnake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([GAME_WIDTH - SPACE_SIZE, GAME_HEIGHT - SPACE_SIZE])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill='blue', tag="pc_snake")
            self.squares.append(square)

    def move(self):
        head_x, head_y = self.coordinates[0]

        # Calculate the direction to move based on the relative positions of the head and food
        if head_x > food.coordinates[0]:
            next_direction = 'left'
        elif head_x < food.coordinates[0]:
            next_direction = 'right'
        elif head_y > food.coordinates[1]:
            next_direction = 'up'
        elif head_y < food.coordinates[1]:
            next_direction = 'down'
        else:
            # If the head is already aligned with the food, maintain the current direction
            next_direction = direction

        # Check if moving in the next direction causes a collision with an obstacle
        next_x, next_y = self.calculate_next_coordinates(next_direction)
        obstacle_collision = any(
            obs_x <= next_x < obs_x + SPACE_SIZE and obs_y <= next_y < obs_y + SPACE_SIZE
            for obs_x, obs_y in obstacle.coordinates
        )

        # If there's a collision, choose a random direction that doesn't collide with an obstacle
        if obstacle_collision:
            possible_directions = ['up', 'down', 'left', 'right']
            possible_directions.remove(direction)
            random.shuffle(possible_directions)
            for possible_direction in possible_directions:
                next_x, next_y = self.calculate_next_coordinates(possible_direction)
                if not any(
                        obs_x <= next_x < obs_x + SPACE_SIZE and obs_y <= next_y < obs_y + SPACE_SIZE
                        for obs_x, obs_y in obstacle.coordinates
                ):
                    next_direction = possible_direction
                    break

        # Move in the chosen direction
        if next_direction == 'left':
            head_x -= SPACE_SIZE
        elif next_direction == 'right':
            head_x += SPACE_SIZE
        elif next_direction == 'up':
            head_y -= SPACE_SIZE
        elif next_direction == 'down':
            head_y += SPACE_SIZE

        self.coordinates.insert(0, (head_x, head_y))
        square = canvas.create_rectangle(head_x, head_y, head_x + SPACE_SIZE, head_y + SPACE_SIZE, fill='blue')
        self.squares.insert(0, square)

        if head_x == food.coordinates[0] and head_y == food.coordinates[1]:
            canvas.delete(food.square)
            food.spawn_food()
        else:
            del self.coordinates[-1]
            canvas.delete(self.squares[-1])
            del self.squares[-1]

    def calculate_next_coordinates(self, direction):
        head_x, head_y = self.coordinates[0]

        if direction == 'left':
            return head_x - SPACE_SIZE, head_y
        elif direction == 'right':
            return head_x + SPACE_SIZE, head_y
        elif direction == 'up':
            return head_x, head_y - SPACE_SIZE
        elif direction == 'down':
            return head_x, head_y + SPACE_SIZE


def next_turn(snake, pc_snake, obstacle):
    global food
    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1
        label.config(text='Score:{}'.format(score))
        canvas.delete(food.square)
        food.spawn_food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    pc_snake.move()

    if check_collisions(snake, obstacle) or check_collisions(snake, pc_snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, pc_snake, obstacle)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake, obstacle):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    for obs_part in obstacle.coordinates:
        obs_x, obs_y = obs_part
        if x >= obs_x and x < obs_x + SPACE_SIZE and y >= obs_y and y < obs_y + SPACE_SIZE:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2,
                       canvas.winfo_height() / 2,
                       font=('consolas', 70),
                       text='GAME OVER',
                       fill='red',
                       tag='gameover')


window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
pc_snake = PCSnake()
obstacle = Obstacle()

global food
food = Food()

next_turn(snake, pc_snake, obstacle)

window.mainloop()
