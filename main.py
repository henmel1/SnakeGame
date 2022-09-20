import random
from tkinter import *

GAME_SIZE = 800
SPEED = 100
SQUARE_SIZE = 50
N_PARTS = 4
SNAKE_COLOR = "#03c6fc"
FOOD_COLOR = "#fc03df"
BG_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = N_PARTS
        self.coordinates = []
        self.parts = []

        for i in range(0, N_PARTS):
            self.coordinates.append([0, (GAME_SIZE/2)-SQUARE_SIZE])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SQUARE_SIZE, y+SQUARE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.parts.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_SIZE/SQUARE_SIZE)-1) * SQUARE_SIZE
        y = random.randint(0, (GAME_SIZE/SQUARE_SIZE)-1) * SQUARE_SIZE
        refresh = False
        for body_part in snake.coordinates:
            if x == body_part[0] and y == body_part[1]:
                refresh = True
        while refresh:
            x = random.randint(0, (GAME_SIZE / SQUARE_SIZE) - 1) * SQUARE_SIZE
            y = random.randint(0, (GAME_SIZE / SQUARE_SIZE) - 1) * SQUARE_SIZE
            refresh = False
            for body_part in snake.coordinates:
                if x == body_part[0] and y == body_part[1]:
                    refresh = True

        self.coordinates = [x,y]

        canvas.create_rectangle(x, y, x+SQUARE_SIZE, y+SQUARE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SQUARE_SIZE
    elif direction == "down":
        y += SQUARE_SIZE
    elif direction == "left":
        x -= SQUARE_SIZE
    elif direction == "right":
        x += SQUARE_SIZE

    snake.coordinates.insert(0, (x,y))

    square = canvas.create_rectangle(x, y, x+SQUARE_SIZE, y+SQUARE_SIZE, fill=SNAKE_COLOR)

    snake.parts.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score+=1

        label.config(text=f"Score: {score}")

        canvas.delete("food")

        food = Food()
        window.after(SPEED, next_turn, snake, food)
    else:
        del snake.coordinates[-1]

        canvas.delete(snake.parts[-1])

        del snake.parts[-1]

        if check_collisions(snake):
            game_over()
        else:
            window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_SIZE:
        return True
    elif y < 0 or y >= GAME_SIZE:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("MS Sans Serif", 80), text = "GAME OVER", fill="#ffffff", tag="gameover")

window = Tk()
window.title("Snake")
window.resizable(False, False)

score = 0
direction = "right"

label = Label(window, text = f"Score: {score}", font=("MS Sans Serif", 40))
label.pack()

canvas = Canvas(window, bg=BG_COLOR, height=GAME_SIZE, width=GAME_SIZE)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("w", lambda event: change_direction("up"))
window.bind("a", lambda event: change_direction("left"))
window.bind("s", lambda event: change_direction("down"))
window.bind("d", lambda event: change_direction("right"))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()

