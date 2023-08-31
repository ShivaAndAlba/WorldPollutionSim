from  random import *
from re import RegexFlag, findall
from tkinter import *
from dataclasses import dataclass


worldMap = [
['S', 'S', 'S', 'S', 'I', 'I', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'F', 'M', 'M', 'M', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'F', 'C', 'S', 'F', 'F', 'C', 'F', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'F', 'F', 'C', 'M', 'M', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'F', 'S', 'S', 'F', 'F', 'C', 'F', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'D', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'F', 'F', 'M', 'M', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'D', 'D', 'S', 'S', 'F', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'F', 'M', 'C', 'M', 'C', 'F', 'C', 'S', 'S', 'S', 'S', 'F', 'C', 'F', 'F', 'F', 'F', 'F', 'D', 'F', 'F', 'F', 'F', 'F', 'F', 'D', 'D', 'D', 'D', 'S', 'S', 'F', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'C', 'F', 'M', 'M', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'F', 'S', 'F', 'F', 'D', 'D', 'D', 'D', 'F', 'F', 'F', 'F', 'D', 'D', 'D', 'D', 'F', 'S', 'F', 'F', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'S', 'C', 'D', 'S', 'F', 'F', 'F', 'F', 'F', 'D', 'F', 'F', 'S', 'S', 'F', 'C', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'S', 'F', 'F', 'F', 'S', 'F', 'F', 'C', 'S', 'S', 'S', 'F', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'M', 'F', 'F', 'C', 'F', 'S', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'D', 'D', 'S', 'S', 'S', 'S', 'F', 'S', 'S', 'S', 'C', 'S', 'F', 'S', 'S', 'F', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'M', 'C', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'S', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'M', 'F', 'C', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'M', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'M', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'D', 'D', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'S', 'S', 'M', 'C', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'D', 'D', 'D', 'D', 'D', 'D', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'I', 'S', 'M', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'C', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'D', 'C', 'C', 'F', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'S', 'S', 'S', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['S', 'S', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'S', 'I', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
['I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I']]


@dataclass
class WorldDiementions:
    length: int
    width: int 
    cellSize: int

    def getCanvasSizeLength(self):
        return self.length*self.cellSize
    
    def getCanvasSizeWidth(self):
        return self.width*self.cellSize

class GlobalWarmingModel():
    def __init__(self, worldDimention):
        self.worldDimention = worldDimention
        self.grid = Grid(self.worldDimention)
        self.guiWin = self.createGui()

    def createGui(self):
        self.root = Tk()
        self.title = self.root.title("Air Polution Model - Ex. 11")
        self.label = Label(self.root)
        self.label.pack()
        self.canvas = Canvas(self.root, height=self.worldDimention.getCanvasSizeWidth(), width=self.worldDimention.getCanvasSizeLength())
        self.canvas.pack()   
        self.addCellsToCanvas() 
        self.root.mainloop()
    
    def addCellsToCanvas(self):
        for y in range(self.worldDimention.width):
            for x in range(self.worldDimention.length):
                cell = self.grid.getCellAt(y, x)
                cell.setCanvasId(self.canvas.create_rectangle(x*self.worldDimention.cellSize,
                                                        y*self.worldDimention.cellSize,
                                                        (x+1)*self.worldDimention.cellSize,
                                                        (y+1)*self.worldDimention.cellSize,
                                                        fill=cell.getColor()))
                cell.setCanvasText(self.canvas.create_text((x + 0.5) * worldDiemention.cellSize,
                                                        (y + 0.5) * worldDiemention.cellSize,
                                                        text=str(cell.getTemprature())))

class Cell():
    def __init__(self, posY, posX) -> None:
        self.posX = posX
        self.posY = posY 
        self.cellType: str
        self.canvasText: Canvas
        self.canvasId: Canvas
        self.color: str
        
        self.norhNeighbor: Cell
        self.southNeighbor: Cell
        self.westNeighbor: Cell
        self.eastNeighbor: Cell

        self.temprature: int
        self.airPolution: int
        self.windDirectin: int
        self.windSpeed: int
        self.clouds: int

        self.cellType = worldMap[self.posY][self.posX]

        if self.cellType == 'F':
            self.color = '#7ed321'
        elif self.cellType == 'I':
            self.color = '#ffffff'
        elif self.cellType == 'C':
            self.color = '#9b9b9b'
        elif self.cellType == 'D':
            self.color = '#f8e71c'
        elif self.cellType == 'S':
            self.color = '#1273de'
        elif self.cellType == 'M':
            self.color = '#1976d2'

        if self.cellType == 'F':
            self.temprature = randint(20, 30)
        elif self.cellType == 'I':
            self.temprature = randint(-30, 0)
        elif self.cellType == 'C':
            self.temprature = randint(20, 40)
        elif self.cellType == 'D':
            self.temprature = randint(30, 40)
        elif self.cellType == 'S':
            self.temprature = randint(10, 20)
        elif self.cellType == 'M':
            self.temprature = randint(0, 10)

        if self.cellType == 'C':
            self.airPolution = 1
        else:
            self.airPolution = 0
    
        self.windDirection = choice(['N', 'S', 'W', 'E'])
        self.windSpeed = randint(0, 30)
    
        self.clouds = choice([True, False])
        if self.clouds:
            if self.cellType == 'F':
                self.color = '#f8e71c'
            elif self.cellType == 'I':
                self.color = '#999999'
            elif self.cellType == 'C':
                self.color = '#9b9b9b'
            elif self.cellType == 'D':
                self.color = '#a19505'
            elif self.cellType == 'S':
                self.color = '#0f477e'
            elif self.cellType == 'M':
                self.color = '#a16707'

    
    def getTemprature(self):
        return self.temprature

    def getAirPolution(self):
        return self.airPolution

    def getWind(self):
        return self.windDirection, self.windSpeed
    
    def getClouds(self):
        return self.clouds

    def getColor(self):
        return self.color

    def setCanvasId(self, canvasId: Canvas):
        self.canvasId = canvasId

    def getCanvasId(self):
        return self.canvasId
    
    def setCanvasText(self, text: str):
        self.canvasText = text

    def getCanvasText(self):
        return self.canvasText

    def getXPosition(self):
        return self.posX
    
    def getYPosition(self):
        return self.posY

    def getNorthNeighbor(self):
       return self.norhNeighbor  

    def setNorthNeighbor(self, neighbor):
       self.norhNeighbor = neighbor 

    def getSouthNeighbor(self):
        return self.southNeighbor

    def setSouthNeighbor(self, neighbor):
        self.southNeighbor = neighbor

    def getWestNeighbor(self):
        return self.westNeighbor

    def setWestNeighbor(self, neighbor):
        self.westNeighbor = neighbor 

    def getEastNeighbor(self):
        return self.eastNeighbor

    def setEastNeighbor(self, neighbor):
        self.eastNeighbor = neighbor

class Grid():
    def __init__(self, dimentions: WorldDiementions) -> None:
        self.dimentions = dimentions
        self.grid = [[self.createCellAt(y,x) for x in range(dimentions.length)] for y in range(dimentions.width)]
        self.updateCellsNeighbors()

    def createCellAt(self, y, x):
        return Cell(y, x)

    def getCellAt(self, y, x):
        return self.grid[y][x]

    def updateCellsNeighbors(self):
        for y in range(self.dimentions.width):
            for x in range(self.dimentions.length):
                currCell = self.getCellAt(y,x)                
                
                if self.cellNorthBound(currCell):
                    currCell.setNorthNeighbor(self.getCellAt(self.dimentions.width - 1, x))
                else:
                    currCell.setNorthNeighbor(self.getCellAt(y-1, x))

                if self.cellSouthBound(currCell):
                    currCell.setSouthNeighbor(self.getCellAt(0, x))
                else:
                    currCell.setSouthNeighbor(self.getCellAt(y+1, x))

                if self.cellWestBound(currCell):
                    currCell.setWestNeighbor(self.getCellAt(y, self.dimentions.length - 1))
                else:
                    currCell.setWestNeighbor(self.getCellAt(y, x-1))

                if self.cellEastBound(currCell):
                    currCell.setEastNeighbor(self.getCellAt(y, 0))
                else:
                    currCell.setEastNeighbor(self.getCellAt(y, x+1))


    def cellNorthBound(self, cell: Cell):
        return cell.getYPosition == 0

    def cellSouthBound(self, cell: Cell):
        return cell.getYPosition() > self.dimentions.width - 2

    def cellWestBound(self, cell: Cell):
        return cell.getXPosition() == 0 

    def cellEastBound(self, cell: Cell):
        return cell.getXPosition() > self.dimentions.length - 2


if __name__ == "__main__":
    worldDiemention = WorldDiementions(length=40, width=20, cellSize=20) 
    GWModel = GlobalWarmingModel(worldDiemention)
