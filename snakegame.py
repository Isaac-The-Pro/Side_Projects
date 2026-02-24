from tkinter import *
from tkinter import ttk

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
canvas = Canvas(root, width=400, height=400, background="white")
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
root.resizable(False, False)

class Snake:
    def __init__(self):
        self.moveDirection = "Right"
        self.segments = []
        self.segments.append(canvas.create_rectangle(100, 100, 120, 120, fill="blue", outline="black"))
    def move(self):
        print("moved")
        if self.moveDirection == "Right":
            canvas.move(self.segments[0], 20, 0)
        elif self.moveDirection == "Left":
            canvas.move(self.segments[0], -20, 0)
        elif self.moveDirection == "Up":
            canvas.move(self.segments[0], 0, -20)
        elif self.moveDirection == "Down":
            canvas.move(self.segments[0], 0, 20)

snake = Snake()

def key_pressed(event):
    if event.keysym == "Left":
        snake.moveDirection = "Left"
    elif event.keysym == "Right":
        snake.moveDirection = "Right"
    elif event.keysym == "Up":
        snake.moveDirection = "Up"
    elif event.keysym == "Down":
        snake.moveDirection = "Down"

root.bind("<Key>", key_pressed)

def schedule_function():
    snake.move()
    root.after(200, schedule_function)

schedule_function()
root.mainloop()
