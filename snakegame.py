from tkinter import *
from tkinter import ttk
import random


class Game:
    def __init__(self):
        self.gridSize = 50
        self.gridWidth = 16
        self.gridHeight = 16
    def lose(self):
        print("Game Over. Your score is: " + str(len(snake.segments)))
        root.destroy()
game = Game()

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
canvas = Canvas(root, width=game.gridWidth*game.gridSize, height=game.gridHeight*game.gridSize, background="white")
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
root.resizable(False, False)

class Snake:
    def __init__(self, startX, startY):
        self.moveDirection = "Right"
        self.moveCoords = [game.gridSize, 0]
        self.segments = []
        self.hitsApple = False
        self.segments.append(canvas.create_rectangle(game.gridSize*startX, game.gridSize*startY, game.gridSize*startX + game.gridSize, game.gridSize*startY + game.gridSize, fill="blue", outline="black"))
        self.canChangeDirection = True
        self.nextDirection = None
    def updateMoveDirection(self, direction):
        if self.canChangeDirection:
            if direction == "Right" and self.moveDirection != "Left":
                self.moveCoords = [game.gridSize, 0]
                self.moveDirection = direction
            if direction == "Left" and self.moveDirection != "Right":
                self.moveCoords = [game.gridSize*-1, 0]
                self.moveDirection = direction
            if direction == "Up" and self.moveDirection != "Down":
                self.moveCoords = [0, game.gridSize*-1]
                self.moveDirection = direction
            if direction == "Down" and self.moveDirection != "Up":
                self.moveCoords = [0, game.gridSize]
                self.moveDirection = direction
            self.nextDirection = None
        else:
            self.nextDirection = direction
        self.canChangeDirection = False
    def move(self):
        self.segments.insert(0, canvas.create_rectangle(canvas.coords(self.segments[0])[0] + self.moveCoords[0], canvas.coords(self.segments[0])[1] + self.moveCoords[1], canvas.coords(self.segments[0])[2] + self.moveCoords[0], canvas.coords(self.segments[0])[3] + self.moveCoords[1], fill="blue", outline="black"))
        for apple in apples:
            if canvas.coords(apple.object) == canvas.coords(snake.segments[0]):
                self.hitsApple = True
                apple.move()
        if not self.hitsApple:
            canvas.delete(self.segments.pop())
        self.hitsApple = False
        for segment in self.segments:
            if canvas.coords(segment) == canvas.coords(self.segments[0]) and segment != self.segments[0]:
                game.lose()
                return
        coords = canvas.coords(self.segments[0])
        if coords[0] < 0 or coords[1] < 0 or coords[2] > game.gridWidth*game.gridSize or coords[3] > game.gridHeight*game.gridSize:
            game.lose()

class Apple:
    def __init__(self, startX, startY):
        self.object = canvas.create_rectangle(game.gridSize*startX, game.gridSize*startY, game.gridSize*startX + game.gridSize, game.gridSize*startY + game.gridSize, fill="red", outline="black")
    def move(self):
        moveOn = False
        while moveOn == False:
            moveOn = True
            x = random.randint(0, game.gridWidth-1)
            y = random.randint(0, game.gridHeight-1)
            for segment in snake.segments:
                snakeX = (canvas.coords(segment)[0])/game.gridSize
                snakeY = (canvas.coords(segment)[1])/game.gridSize
                if snakeX == x and snakeY == y:
                    moveOn = False
        canvas.moveto(self.object, x*game.gridSize-1, y*game.gridSize-1)


snake = Snake(4, 8)
apples = [Apple(8, 8), Apple(6, 6), Apple(6, 10), Apple(10, 6), Apple(10, 10)]

def key_pressed(event):
    directions = ["Left", "Right", "Up", "Down"]
    if event.keysym in directions:
        snake.updateMoveDirection(event.keysym)

root.bind("<Key>", key_pressed)

def schedule_function():
    snake.canChangeDirection = True
    snake.move()
    if snake.nextDirection:
        snake.updateMoveDirection(snake.nextDirection)
    root.after(150, schedule_function)

schedule_function()
root.mainloop()
