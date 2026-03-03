from tkinter import *
import math
import random

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
        for x in range(self.minesX):
           rowTiles = []
           for y in range(self.minesY):
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
                tile.createNumber(self.tiles.index(row), row.index(tile), self.tiles, self.canvas, self.tileWidth)
                self.canvas.tag_raise(tile)
    def leftClick(self, event):
        for row in self.tiles:
            for tile in row:
                xy = self.canvas.coords(tile.object)
                if (xy[0] <= event.x <= xy[2]) and (xy[1] <= event.y <= xy[3]):
                    tile.click(game.canvas)

               
class Tile:
    def __init__(self, x, y, width, canvas):
       self.x = x
       self.y = y
       self.realX = x*width
       self.realY = y*width
       self.object = canvas.create_rectangle(self.realX, self.realY, self.realX + width, self.realY + width, fill="gray", outline="black")
       self.hasMine = False
       self.touchesMines = 0
    def click(self, canvas):
        canvas.itemconfig(self.object, state='hidden')
    def createNumber(self, listX, listY, tiles, canvas, tileWidth):
        self.numOfMines = 0
        if self.hasMine == False:
            self.surroundingTiles = []
            try:
                self.surroundingTiles.append(tiles[listX+1][listY])
            except:
                pass
            try:
                self.surroundingTiles.append(tiles[listX-1][listY])
            except:
                pass
            try:
                self.surroundingTiles.append(tiles[listX][listY+1])
            except:
                pass
            try:
                self.surroundingTiles.append(tiles[listX][listY-1])
            except:
                pass
            try:
                self.surroundingTiles.append(tiles[listX+1][listY+1])
            except:
                pass
            try:
                self.surroundingTiles.append(tiles[listX+1][listY-1])
            except:
                pass
            try:
                self.surroundingTiles.append(tiles[listX-1][listY+1])
            except:
                pass
            try:
                self.surroundingTiles.append(tiles[listX-1][listX-1])
            except:
                pass
            for tile in self.surroundingTiles:
                if tile.hasMine == True:
                    self.numOfMines += 1
        if self.numOfMines != 0:
            self.label = canvas.create_text(listX*tileWidth+tileWidth/2, listY*tileWidth+tileWidth/2, text=self.numOfMines)

class Mine:
    def __init__(self, x, y, width, canvas):
        self.x = x
        self.y = y
        self.realX = x*width
        self.realY = y*width
        self.object = canvas.create_rectangle(self.realX, self.realY, self.realX + width, self.realY + width, fill="red", outline="black")

def click_handler(event):
    if event.num == 1:
        game.leftClick(event)

game = Game(20, 20, 20)

root.bind("<Button>", click_handler)
root.mainloop()
