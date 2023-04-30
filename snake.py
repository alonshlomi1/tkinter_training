import random
import tkinter as tk

GRID_SIZE = 30
WIN_WIDTH = 800
WIN_HEIGHT = 800
SPEED = 100
SPACE_SIZE = 50
SNAKE_SIZE = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "YELLOW"
BG_COLOR = "BLACK"


class Snake:

    def __init__(self):
        self.size = SNAKE_SIZE
        self.xy = []
        self.squares = []
        for i in range(0, SNAKE_SIZE):
            self.xy.append([0, 0])

        for x, y in self.xy:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                             fill=SNAKE_COLOR,
                                             tags="snake"
                                             )
            self.squares.append(square)


class Food:

    def __init__(self):
        x = random.randint(0, (WIN_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (WIN_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.xy = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                           fill=FOOD_COLOR,
                           tags="food"
                           )


def next_move(snake, food):
    x, y = snake.xy[0]
    if direction == "U":
        y -= SPACE_SIZE
    elif direction == "D":
        y += SPACE_SIZE
    elif direction == "L":
        x -= SPACE_SIZE
    else:
        x += SPACE_SIZE

    snake.xy.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")

    snake.squares.insert(0, square)

    if x == food.xy[0] and y == food.xy[1]:
        global score
        score += 1
        label.configure(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.xy[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_valid_move(snake):
        game_over()
    else:
        root.after(SPEED, next_move, snake, food)


def change_move_direction(new_direction):
    global direction

    if new_direction == "U" and direction != "D":
        direction = new_direction
    if new_direction == "D" and direction != "U":
        direction = new_direction
    if new_direction == "R" and direction != "L":
        direction = new_direction
    if new_direction == "L" and direction != "R":
        direction = new_direction


def check_valid_move(snake):
    x, y = snake.xy[0]

    if x < 0 or x >= WIN_WIDTH or y < 0 or y >= WIN_HEIGHT:
        return True

    for part in snake.xy[1:]:
        if x == part[0] and y == part[1]:
            return True

    return False


def game_over():
    global game_over_flag
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, text="Game Over", fill="red",
                       font=("Arial", 50), tags="game_over")
    game_over_flag = 1

def restart():
    global game_over_flag
    print(game_over_flag)
    if game_over_flag:
        global snake
        global food
        global direction
        global score
        snake = None
        food = None
        canvas.delete(tk.ALL)
        snake = Snake()
        food = Food()
        game_over_flag = 0
        direction = "D"
        score = 0
        label.configure(text="Score: {}".format(score))
        next_move(snake, food)




root = tk.Tk()
root.title("Snake Game")
root.resizable(False, False)
game_over_flag = 0
score = 0
direction = "D"
button = tk.Button(root, text="Restart")
button.pack()
button.bind("<Button-1>", lambda event: restart())
button.bind("<Return>", lambda event: restart())

label = tk.Label(
    root,
    text="Score: {}".format(score),
    font=("Arial", 20)
)
label.pack()

canvas = tk.Canvas(
    root,
    bg=BG_COLOR,
    height=WIN_HEIGHT,
    width=WIN_WIDTH
)
canvas.pack()

root.update()
win_width = root.winfo_width()
win_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width / 2) - (win_width / 2))
y = int((screen_height / 2) - (win_height / 2))

root.geometry(f"{win_width}x{win_height}+{x}+{y}")

root.bind('<Left>', lambda event: change_move_direction("L"))
root.bind('<Right>', lambda event: change_move_direction("R"))
root.bind('<Up>', lambda event: change_move_direction("U"))
root.bind('<Down>', lambda event: change_move_direction("D"))

snake = Snake()
food = Food()

next_move(snake, food)

root.mainloop()
