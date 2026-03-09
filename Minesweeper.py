from tkinter import *
import math
import random
import sys
sys.setrecursionlimit(100000000)
class Game:
    def __init__(self, minesX, minesY, tileWidth):
        self.minesX = minesX
        self.minesY = minesY
        self.tileWidth = tileWidth
        global root
        root = Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.canvas = Canvas(root, width=self.minesX*tileWidth, height=self.minesY*tileWidth, background="white")
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        root.resizable(False, False)
        self.tiles = []
        self.isRunning = True
        for y in range(self.minesX):
           rowTiles = []
           for x in range(self.minesY):
               rowTiles.append(Tile(x, y, self.tileWidth, self.canvas))
           self.tiles.append(rowTiles)
        self.numOfMines = math.floor(minesX*minesY / 6.4)
        self.mines = []
        self.tilesWithoutMines = []
        for row in self.tiles:
            for tile in row:
                self.tilesWithoutMines.append(tile)
        for i in range(self.numOfMines):
            tile = random.choice(self.tilesWithoutMines)
            self.mines.append(Mine(tile.x, tile.y, tileWidth, self.canvas))
            tile.hasMine = True
            self.tilesWithoutMines.remove(tile)
        for mine in self.mines:
            self.canvas.tag_lower(mine.object)
        for row in self.tiles:
            for tile in row:
                tile.createNumber(row.index(tile), self.tiles.index(row), self.tiles, self.canvas, self.tileWidth)
                self.canvas.tag_raise(tile.object)
    def leftClick(self, event):
        for row in self.tiles:
            for tile in row:
                xy = self.canvas.coords(tile.object)
                if (xy[0] <= event.x <= xy[2]) and (xy[1] <= event.y <= xy[3]):
                    tile.click(game.canvas)
                    return
    def rightClick(self, event):
        for row in self.tiles:
            for tile in row:
                xy = self.canvas.coords(tile.object)
                if (xy[0] <= event.x <= xy[2]) and (xy[1] <= event.y <= xy[3]):
                    tile.addFlag(game.canvas)
    def lose(self):
        root.destroy()
        print("game over")
    def win(self):
        root.destroy()
        print("you won!")
        self.isRunning = False
               
class Tile:
    def __init__(self, x, y, width, canvas):
       self.x = x
       self.y = y
       self.realX = x*width
       self.realY = y*width
       self.object = canvas.create_rectangle(self.realX, self.realY, self.realX + width, self.realY + width, fill="gray", outline="black")
       self.hasMine = False
       self.touchesMines = 0
       self.clicked=False
       self.flag=None
       self.flag = canvas.create_oval(self.realX+width/4, self.realY+width/4, self.realX+3*width/4, self.realY+3*width/4, fill="red", state='hidden')
       self.hasFlag = False
    def click(self, canvas):
        canvas.itemconfig(self.object, state='hidden')
        self.clicked=True
        self.getSurroundingTiles(self.listX, self.listY, self.tiles)
        for tile in self.surroundingTiles:
            if self.numOfMines==0 and tile.clicked==False:
                tile.click(canvas)
        if self.flag:
            canvas.itemconfig(self.flag, state='hidden')
        if self.hasMine == True and self.hasFlag == False:
            game.lose()
    def getSurroundingTiles(self, listX, listY, tiles):
        self.surroundingTiles = []
        try:
            self.surroundingTiles.append(tiles[listY+1][listX])
        except:
            pass
        try: 
            self.surroundingTiles.append(tiles[listY][listX+1])
        except:
            pass
        try:
            self.surroundingTiles.append(tiles[listY+1][listX+1])
        except:
            pass
        if listY != 0:
            self.surroundingTiles.append(tiles[listY-1][listX])
            try:
                self.surroundingTiles.append(tiles[listY-1][listX+1])
            except:
                pass
        if listX !=0:
            self.surroundingTiles.append(tiles[listY][listX-1])
            try:
                self.surroundingTiles.append(tiles[listY+1][listX-1])
            except:
                pass
        if listX != 0 and listY!=0:
            self.surroundingTiles.append(tiles[listY-1][listX-1])
        return self.surroundingTiles
    def createNumber(self, listX, listY, tiles, canvas, tileWidth):
        self.numOfMines = 0
        if self.hasMine == False:
            self.getSurroundingTiles(listX, listY, tiles)
            for tile in self.surroundingTiles:
                if tile.hasMine == True:
                    self.numOfMines += 1
        if self.numOfMines != 0:
            self.label = canvas.create_text(listX*tileWidth+tileWidth/2, listY*tileWidth+tileWidth/2, text=self.numOfMines)
        self.listX = listX
        self.listY = listY
        self.tiles = tiles
    def addFlag(self, canvas):
        print("addflag called")
        if self.hasFlag == False:
                canvas.itemconfig(self.flag, state='normal')
                self.hasFlag = True
        else:
                canvas.itemconfig(self.flag, state='hidden')
                self.hasFlag = False
            
class Mine:
    def __init__(self, x, y, width, canvas):
        self.x = x
        self.y = y
        self.realX = x*width
        self.realY = y*width
        self.object = canvas.create_rectangle(self.realX, self.realY, self.realX + width, self.realY + width, fill="red", outline="black")

def click_handler(event):
    try:
        if event.num == 1:
            game.leftClick(event)
            winGame = True
            for row in game.tiles:
                for tile in row:
                    if tile.hasMine == False and tile.clicked == False:
                        winGame = False
            if winGame:
                game.win()
        elif event.num == 3:
            game.rightClick(event)
    except:
        pass
game = Game(20, 20, 40)

root.bind("<Button>", click_handler)
root.mainloop()
