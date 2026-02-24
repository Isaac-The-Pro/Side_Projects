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
        elif self.moveDirection =="Left":
            canvas.move(self.segments[0], -20, 0)
snake = Snake()
def key_pressed(event):
    print("Key was pressed")
    if event.keysym == "Left":
        print("Left arrow pressed")
        snake.moveDirection = "Left"

root.bind("<Key>", key_pressed)

def schedule_function():
    snake.move()
    root.after(1000, schedule_function)

schedule_function()
root.mainloop()
