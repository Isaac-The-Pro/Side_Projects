from tkinter import *
import random

class Game:
    def __init__(self):
        self.gridSize = 30
        self.gridWidth = 16
        self.gridHeight = 16
        self.squares = []
        for x in range(self.gridWidth):
            column = []
            for y in range(self.gridHeight):
                column.append(Square(x, y))
            self.squares.append(column)
        self.snakeSize = self.gridSize*0.8
        self.snakeGap = self.gridSize*0.1
        self.framerate = 10
    def lose(self):
        print("Game Over. Your score is: " + str(len(snake.segments) -1))
        root.destroy()
    def win(self):
        print("You Won!")
        root.destroy()
        return
    
class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hasSnake = False
        self.hasApple = False
    def draw(self, canvas):
        if ((self.x + self.y) % 2) == 0:
            self.object = canvas.create_rectangle(game.gridSize*self.x, game.gridSize*self.y, game.gridSize*self.x + game.gridSize, game.gridSize*self.y + game.gridSize, fill="#00aa00", width=0)
        else:
            self.object = canvas.create_rectangle(game.gridSize*self.x, game.gridSize*self.y, game.gridSize*self.x + game.gridSize, game.gridSize*self.y + game.gridSize, fill="#009900", width=0)
game = Game()
root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
canvas = Canvas(root, width=game.gridWidth*game.gridSize, height=game.gridHeight*game.gridSize, background="white")
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
root.resizable(False, False)
for column in game.squares:
    for square in column:
        square.draw(canvas)


class Snake:
    def __init__(self, startX, startY):
        self.moveDirection = None
        self.moveCoords = [game.gridSize, 0]
        self.hitsApple = False
        self.segments = [canvas.create_oval(game.gridSize*startX + game.snakeGap, game.gridSize*startY + game.snakeGap, game.gridSize*startX + game.gridSize - game.snakeGap, game.gridSize*startY + game.gridSize - game.snakeGap, fill="blue", width=0)]
        self.canChangeDirection = True
        self.nextDirection = None
        self.lines = []
        self.backMoveCoords = None
        self.canMove = False
    def updateMoveDirection(self, direction):
        if self.canChangeDirection:
            if direction == "Right" and self.moveDirection != "Left":
                self.nextMoveCoords = [game.gridSize, 0]
                self.moveDirection = direction
            if direction == "Left" and self.moveDirection != "Right":
                self.nextMoveCoords = [game.gridSize*-1, 0]
                self.moveDirection = direction
            if direction == "Up" and self.moveDirection != "Down":
                self.nextMoveCoords = [0, game.gridSize*-1]
                self.moveDirection = direction
            if direction == "Down" and self.moveDirection != "Up":
                self.nextMoveCoords = [0, game.gridSize]
                self.moveDirection = direction
            self.nextDirection = None
        else:
            self.nextDirection = direction
        self.canChangeDirection = False
    def preMove(self):
        self.canMove = True
        self.moveCoords = self.nextMoveCoords
        nextCoords = [canvas.coords(self.segments[0])[0] + self.moveCoords[0], canvas.coords(self.segments[0])[1] + self.moveCoords[1], canvas.coords(self.segments[0])[2] + self.moveCoords[0], canvas.coords(self.segments[0])[3] + self.moveCoords[1]]
        if nextCoords[0] < 0 or nextCoords[1] < 0 or nextCoords[2] >game.gridWidth*game.gridSize or nextCoords[3] > game.gridHeight*game.gridSize:
            game.lose()
            return
        
        self.hitsApple = False
        for apple in apples:
            if canvas.coords(apple.object) == nextCoords:
                self.hitsApple = True
                self.appleHit = apple
        if not self.hitsApple:
            game.squares[int(canvas.coords(self.segments[len(self.segments)-1])[0]/game.gridSize)][int(canvas.coords(self.segments[len(self.segments)-1])[1]/game.gridSize)].hasSnake = False
        
        self.backMoveCoords = [(canvas.coords(self.segments[len(self.segments) - 2])[0] - canvas.coords(self.segments[len(self.segments) - 1])[0]), (canvas.coords(self.segments[len(self.segments) - 2])[1] - canvas.coords(self.segments[len(self.segments) - 1])[1])]

        self.segments.insert(0, canvas.create_oval(canvas.coords(self.segments[0])[0], canvas.coords(self.segments[0])[1], canvas.coords(self.segments[0])[2], canvas.coords(self.segments[0])[3], fill="blue", width=0))

    def move(self):
        if self.canMove:
            canvas.move(self.segments[0], self.moveCoords[0]/game.framerate, self.moveCoords[1]/game.framerate)
            if not self.hitsApple:
                canvas.move(self.segments[len(self.segments) - 1], self.backMoveCoords[0]/game.framerate, self.backMoveCoords[1]/game.framerate)
            for i in range(len(self.lines)):
                canvas.delete(self.lines.pop()) 
            for i in range(len(self.segments) - 1):
                self.lines.append(canvas.create_line(canvas.coords(self.segments[i])[0] + game.snakeSize/2, canvas.coords(self.segments[i])[1] + game.snakeSize/2, canvas.coords(self.segments[i + 1])[0] + game.snakeSize/2, canvas.coords(self.segments[i + 1])[1] + game.snakeSize/2, width=game.snakeSize, fill="blue"))
        
    def postMove(self):
        if self.canMove:
            game.squares[int(canvas.coords(self.segments[0])[0]/game.gridSize)][int(canvas.coords(self.segments[0])[1]/game.gridSize)].hasSnake = True
            if not self.hitsApple:
                game.squares[int(canvas.coords(self.segments[len(self.segments)-1])[0]/game.gridSize)][int(canvas.coords(self.segments[len(self.segments)-1])[1]/game.gridSize)].hasSnake = False
                canvas.delete(self.segments.pop())
            else:
                self.appleHit.move()
            
            for segment in self.segments:
                if canvas.coords(segment) == canvas.coords(self.segments[0]) and segment != self.segments[0]:
                    game.lose()
                    return
            
class Apple:
    def __init__(self, startX, startY):
        self.object = canvas.create_oval(game.gridSize*startX + game.snakeGap, game.gridSize*startY + game.snakeGap, game.gridSize*startX + game.gridSize - game.snakeGap, game.gridSize*startY + game.gridSize - game.snakeGap, fill="red", outline="black")
    def move(self):
        availableSpaces = []
        for x in range(len(game.squares)):
            for y in range(len(game.squares[x])):
                if game.squares[x][y].hasSnake == False and game.squares[x][y].hasApple == False:
                    availableSpaces.append([x, y])
        if len(availableSpaces) != 0:
            space = random.choice(availableSpaces)
            game.squares[int(canvas.coords(self.object)[0]/game.gridSize)][int(canvas.coords(self.object)[1]/game.gridSize)].hasApple = False
            canvas.moveto(self.object, space[0]*game.gridSize-1 + game.snakeGap, space[1]*game.gridSize-1 + game.snakeGap)
            game.squares[space[0]][space[1]].hasApple = True
        else:
            canvas.delete(self.object)


snake = Snake(1, 4)
appleX = 5
appleY = 4
apples = [Apple(appleX, appleY), Apple(appleX + 2, appleY + 2), Apple(appleX - 2, appleY + 2), Apple(appleX + 2, appleY - 2), Apple(appleX - 2, appleY - 2)]

def key_pressed(event):
    directions = ["Left", "Right", "Up", "Down"]
    if event.keysym in directions:
        snake.updateMoveDirection(event.keysym)

root.bind("<Key>", key_pressed)

game.loops = 0
def schedule_function():
    if game.loops % game.framerate == 0:
        snake.canChangeDirection = True
        if snake.moveDirection:
            snake.preMove()
        if snake.nextDirection:
            snake.updateMoveDirection(snake.nextDirection)
        if len(snake.segments) == (game.gridHeight*game.gridWidth):
            game.win()
            return
    if snake.moveDirection:
        snake.move()
        if game.loops % game.framerate == game.framerate - 1:
            snake.postMove()
    game.loops += 1
    if game.loops > game.framerate:
        game.loops = game.loops % game.framerate
    root.after(15, schedule_function)

schedule_function()
root.mainloop()
