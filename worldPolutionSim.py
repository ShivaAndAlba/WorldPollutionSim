from re import RegexFlag, findall
import tkinter as tk
from dataclasses import dataclass
import random as rd

worldMap = [
    ['S', 'S', 'S', 'S', 'I', 'I', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'I', 'I',
        'I', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'I', 'I',
        'I', 'I', 'I', 'I', 'I', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F',
        'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'F', 'M', 'M', 'M', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'F', 'C', 'S', 'F', 'F', 'C',
        'F', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'F', 'F', 'C', 'M', 'M', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'F', 'S', 'S', 'F', 'F', 'C',
        'F', 'C', 'C', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'D', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'F', 'F', 'M', 'M', 'F', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'F', 'F', 'F', 'F',
        'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'D', 'D', 'S', 'S', 'F', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'F', 'M', 'C', 'M', 'C', 'F', 'C', 'S', 'S', 'S', 'S', 'F', 'C', 'F', 'F', 'F',
        'F', 'F', 'D', 'F', 'F', 'F', 'F', 'F', 'F', 'D', 'D', 'D', 'D', 'S', 'S', 'F', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'C', 'F', 'M', 'M', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'F', 'S', 'F', 'F',
        'D', 'D', 'D', 'D', 'F', 'F', 'F', 'F', 'D', 'D', 'D', 'D', 'F', 'S', 'F', 'F', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F',
        'S', 'C', 'D', 'S', 'F', 'F', 'F', 'F', 'F', 'D', 'F', 'F', 'S', 'S', 'F', 'C', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'D', 'D', 'D',
        'C', 'C', 'D', 'S', 'F', 'F', 'F', 'S', 'F', 'F', 'C', 'S', 'S', 'S', 'F', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'S', 'M', 'F', 'F', 'C', 'F', 'S', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'D',
        'D', 'S', 'S', 'S', 'S', 'F', 'S', 'S', 'S', 'C', 'S', 'F', 'S', 'S', 'F', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'S', 'M', 'C', 'F', 'F', 'F', 'F', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'D',
        'D', 'D', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'S', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'S', 'M', 'F', 'C', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'F',
        'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'S', 'M', 'F', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F', 'F',
        'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'M', 'F', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F',
        'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'D', 'D', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'M', 'C', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'F',
        'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'F', 'D', 'D', 'D', 'D', 'D', 'D', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'I', 'S', 'M', 'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'C',
        'F', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'D', 'C', 'C', 'F', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'S', 'S', 'S', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S',
        'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['S', 'S', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'I', 'I', 'I', 'I', 'S', 'S', 'S', 'I',
        'I', 'I', 'I', 'S', 'S', 'S', 'S', 'I', 'I', 'I', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    ['I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I']]


@dataclass
class WorldDiementions:
    length: int
    width: int
    cell_size: int

    def get_cell_length(self):
        """returns cell length"""
        return self.length*self.cell_size

    def get_cell_width(self):
        """returns cell width"""
        return self.width*self.cell_size


class GlobalWarmingModel():
    """singelton class to handle all model functionality"""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GlobalWarmingModel, cls).__new__(cls)
        return cls.instance

    def __init__(self, world_dimention):
        self.world_dimention = world_dimention
        self.grid = Grid(self.world_dimention)

        """ creates gui via tkinter"""
        self.root = tk.Tk()
        self.title = self.root.title("Air Polution Model - Ex. 11")
        self.label = tk.Label(self.root)
        self.label.pack()
        self.canvas = tk.Canvas(self.root,
                                height=self.world_dimention.get_cell_width(),
                                width=self.world_dimention.get_cell_length())
        self.canvas.pack()
        self.insert_cell()
        self.root.mainloop()

    def insert_cell(self):
        """create and insert cells to canvas"""
        for y in range(self.world_dimention.width):
            for x in range(self.world_dimention.length):
                cell = self.grid.getCellAt(y, x)
                cell.set_canvas_id(
                    self.canvas.create_rectangle(
                        x*self.world_dimention.cell_size,
                        y*self.world_dimention.cell_size,
                        (x+1)*self.world_dimention.cell_size,
                        (y+1)*self.world_dimention.cell_size,
                        fill=cell.get_color()))
                cell.set_canvas_text(
                    self.canvas.create_text(
                        (x + 0.5) * worldDiemention.cell_size,
                        (y + 0.5) *
                        worldDiemention.cell_size,
                        text=str(cell.get_temprature())))


# TODO: need to redisgn this unreadable class
#  change to: abstract factory of cells which creates
#  cells factory of position, graphics and type
#  neighbors factory of up, down, left, rigth
#  current forcast

class Cell():
    """creates cell with a position, type and souraounding cell neighborhood"""

    def __init__(self, pos_y, pos_x) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cell_type: str
        self.canvas_text: tk.Canvas
        self.canvas_id: tk.Canvas
        self.color: str

        self.norh_neighbor: Cell
        self.south_neighbor: Cell
        self.west_neighbor: Cell
        self.east_neighbor: Cell

        self.temprature: int
        self.air_polution: int
        self.wind_directin: int
        self.wind_speed: int
        self.clouds: int

        self.cell_type = worldMap[self.pos_y][self.pos_x]

        if self.cell_type == 'F':
            self.color = '#7ed321'
        elif self.cell_type == 'I':
            self.color = '#ffffff'
        elif self.cell_type == 'C':
            self.color = '#9b9b9b'
        elif self.cell_type == 'D':
            self.color = '#f8e71c'
        elif self.cell_type == 'S':
            self.color = '#1273de'
        elif self.cell_type == 'M':
            self.color = '#1976d2'

        if self.cell_type == 'F':
            self.temprature = rd.randint(20, 30)
        elif self.cell_type == 'I':
            self.temprature = rd.randint(-30, 0)
        elif self.cell_type == 'C':
            self.temprature = rd.randint(20, 40)
        elif self.cell_type == 'D':
            self.temprature = rd.randint(30, 40)
        elif self.cell_type == 'S':
            self.temprature = rd.randint(10, 20)
        elif self.cell_type == 'M':
            self.temprature = rd.randint(0, 10)

        if self.cell_type == 'C':
            self.air_polution = 1
        else:
            self.air_polution = 0

        self.wind_direction = rd.choice(['N', 'S', 'W', 'E'])
        self.wind_speed = rd.randint(0, 30)

        self.clouds = rd.choice([True, False])
        if self.clouds:
            if self.cell_type == 'F':
                self.color = '#f8e71c'
            elif self.cell_type == 'I':
                self.color = '#999999'
            elif self.cell_type == 'C':
                self.color = '#9b9b9b'
            elif self.cell_type == 'D':
                self.color = '#a19505'
            elif self.cell_type == 'S':
                self.color = '#0f477e'
            elif self.cell_type == 'M':
                self.color = '#a16707'

    def get_temprature(self):
        return self.temprature

    def get_air_polution(self):
        return self.air_polution

    def get_wind(self):
        return self.wind_direction, self.wind_speed

    def get_clouds(self):
        return self.clouds

    def get_color(self):
        return self.color

    def set_canvas_id(self, canvasId: tk.Canvas):
        self.canvas_id = canvasId

    def get_canvas_id(self):
        return self.canvas_id

    def set_canvas_text(self, text: str):
        self.canvas_text = text

    def get_canvas_text(self):
        return self.canvas_text

    def get_x_position(self):
        return self.pos_x

    def get_y_position(self):
        return self.pos_y

    def get_north_neighbor(self):
        return self.norh_neighbor

    def set_north_neighbor(self, neighbor):
        self.norh_neighbor = neighbor

    def get_south_neighbor(self):
        return self.south_neighbor

    def set_south_neighbor(self, neighbor):
        self.south_neighbor = neighbor

    def get_west_neighbor(self):
        return self.west_neighbor

    def set_west_neighbor(self, neighbor):
        self.west_neighbor = neighbor

    def get_east_neighbor(self):
        return self.east_neighbor

    def set_east_neighborr(self, neighbor):
        self.east_neighbor = neighbor


class Grid():
    def __init__(self, dimentions: WorldDiementions) -> None:
        self.dimentions = dimentions
        self.grid = [[self.createCellAt(y, x) for x in range(
            dimentions.length)] for y in range(dimentions.width)]
        self.updateCellsNeighbors()

    def createCellAt(self, y, x):
        return Cell(y, x)

    def getCellAt(self, y, x):
        return self.grid[y][x]

    def updateCellsNeighbors(self):
        for y in range(self.dimentions.width):
            for x in range(self.dimentions.length):
                currCell = self.getCellAt(y, x)

                if self.cellNorthBound(currCell):
                    currCell.set_north_neighbor(
                        self.getCellAt(self.dimentions.width - 1, x))
                else:
                    currCell.set_north_neighbor(self.getCellAt(y-1, x))

                if self.cellSouthBound(currCell):
                    currCell.set_south_neighbor(self.getCellAt(0, x))
                else:
                    currCell.set_south_neighbor(self.getCellAt(y+1, x))

                if self.cellWestBound(currCell):
                    currCell.set_west_neighbor(
                        self.getCellAt(y, self.dimentions.length - 1))
                else:
                    currCell.set_west_neighbor(self.getCellAt(y, x-1))

                if self.cellEastBound(currCell):
                    currCell.set_east_neighborr(self.getCellAt(y, 0))
                else:
                    currCell.set_east_neighborr(self.getCellAt(y, x+1))

    def cellNorthBound(self, cell: Cell):
        return cell.get_y_position == 0

    def cellSouthBound(self, cell: Cell):
        return cell.get_y_position() > self.dimentions.width - 2

    def cellWestBound(self, cell: Cell):
        return cell.get_x_position() == 0

    def cellEastBound(self, cell: Cell):
        return cell.get_x_position() > self.dimentions.length - 2


if __name__ == "__main__":
    worldDiemention = WorldDiementions(length=40, width=20, cell_size=20)
    GWModel = GlobalWarmingModel(worldDiemention)
