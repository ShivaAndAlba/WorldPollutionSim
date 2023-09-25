from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from random import randint

import numpy as np

from states import City, Desert, Forest, Ice, Mountain, Sea
from worldMap import worldMap


@dataclass
class WorldDiementions:
    cell_num_length: int
    cell_num_width: int
    cell_size: int

    @property
    def length(self):
        """returns cell length"""
        return self.cell_num_length * self.cell_size

    @property
    def width(self):
        """returns cell width"""
        return self.cell_num_width * self.cell_size


class GlobalWarmingModel:
    gui: Gui

    def __init__(self):
        self.gui = Gui()
        self.gui.init_grid()
        self.gui.init_cell_canvas()
        self.gui.init_cell_neighbors()
        self.gui.tk_mainloop()


class Gui:
    def __init__(self):
        """creates gui via tkinter"""
        self.root = tk.Tk()
        self.title = self.root.title("Air Polution Model - Ex. 11")
        self.label = tk.Label(self.root)
        self.label.pack()
        self._canvas = tk.Canvas(
            self.root,
            height=g_world_diemention.width,
            width=g_world_diemention.length,
        )
        self._canvas.pack()

    def tk_mainloop(self):
        self.root.mainloop()

    @property
    def canvas(self):
        return self._canvas

    def init_grid(self):
        self.grid = Grid()

    def init_cell_canvas(self):
        self.grid.cell_canvas_matx = [
            [
                CellCanvas(self, self.grid.cell_at(y, x), g_world_diemention.cell_size)
                for x in range(g_world_diemention.cell_num_length)
            ]
            for y in range(g_world_diemention.cell_num_width)
        ]

    def init_cell_neighbors(self):
        self.grid.init_cell_neighbors()


class Grid(Gui):
    """two dimenional array of cellls
    manages creation and updates of each cell state"""

    cell_obj_matx: list[list[Cell]]

    def __init__(self):
        self.cell_obj_matx = [
            [
                Cell((x, y), worldMap[y][x])
                for x in range(g_world_diemention.cell_num_length)
            ]
            for y in range(g_world_diemention.cell_num_width)
        ]

    @property
    def cell_canvas_matx(self):
        return self._cell_canvas_matrix

    @cell_canvas_matx.setter
    def cell_canvas_matx(self, mat: list[list[CellCanvas]]):
        self._cell_canvas_matrix = mat

    def init_cell_neighbors(self):
        for y in range(len(self.cell_obj_matx)):
            for x in range(y):
                self.cell_at(x, y).neighbors_init(self)

    def cell_at(self, point_y, point_x):
        return self.cell_obj_matx[point_y][point_x]


# TODO: this class should be part of Cell class
class CellCanvas(Gui):
    def __init__(self, gui: Gui, cell: Cell, cell_size: int):
        self.gui = gui
        self.cell_size = cell_size
        self.cell = cell
        self.draw_cell()

    def draw_cell(self):
        self.gui.canvas.create_rectangle(
            self.cell.x_cord * self.cell_size,
            self.cell.y_cord * self.cell_size,
            (self.cell.x_cord + 1) * self.cell_size,
            (self.cell.y_cord + 1) * self.cell_size,
            fill=self.cell_color(),
        )

    def cell_color(self) -> str:
        return self.cell.state.state_color

    def text(self, text):
        self.gui.canvas.create_text(
            (self.cell.x_cord + 0.5) * self.cell_size,
            (self.cell.y_cord + 0.5) * self.cell_size,
            text=str(text),
        )


class Neighborhood(Grid):
    """handels all cell's neighbors data"""

    def __init__(self, cell: Cell, grid: Grid):
        self.grid = grid
        self.set_north(cell)
        self.set_south(cell)
        self.set_west(cell)
        self.set_east(cell)

    def cell_north_bound(self, cell: Cell):
        """checks if cell is at the top of the grid"""
        return cell.y_cord == 0

    def cell_south_bound(self, cell: Cell):
        """check if cell is at the bottom of the grid"""
        return cell.y_cord > g_world_diemention.cell_num_width - 2

    def cell_west_bound(self, cell: Cell):
        """check if cell is at the rightest of the grid"""
        return cell.x_cord == 0

    def cell_east_bound(self, cell: Cell):
        """check if cell is the leftest of the grid"""
        return cell.x_cord > g_world_diemention.cell_num_length - 2

    @property
    def north(self):
        return self._north

    def set_north(self, cell: Cell):
        if self.cell_north_bound(cell):
            y_cord = g_world_diemention.cell_num_width - 1
        else:
            y_cord = cell.y_cord - 1

        self._north = self.grid.cell_at(y_cord, cell.x_cord)

    @property
    def south(self):
        return self._south

    def set_south(self, cell: Cell):
        if self.cell_south_bound(cell):
            y_cord = 0
        else:
            y_cord = cell.y_cord + 1

        self._south = self.grid.cell_at(y_cord, cell.x_cord)

    @property
    def west(self):
        return self._west

    def set_west(self, cell: Cell):
        if self.cell_west_bound(cell):
            x_cord = g_world_diemention.cell_num_length - 1
        else:
            x_cord = cell.x_cord - 1

        self._west = self.grid.cell_at(cell.y_cord, x_cord)

    @property
    def east(self):
        return self._east

    def set_east(self, cell: Cell):
        if self.cell_east_bound(cell):
            x_cord = 0
        else:
            x_cord = cell.x_cord + 1

        self._east = self.grid.cell_at(cell.y_cord, x_cord)

    def everyone(self) -> dict[str, Cell]:
        return {"N": self.north, "S": self.south, "W": self.west, "E": self.east}

    def mean_of(self, prop: str) -> int:
        return np.mean([temp.__dict__[prop] for temp in self.everyone().values()])


class Cell:
    """
    A class describing single cell in cellular automata.
    Cells are state machines that change states according to cells weather.
    ...
    Atributes
    ---------
    neighbors : Neighborhood
        cell's neighbors from N,S,W,E

    x_cord: int
    y_cord: int
        cell's coordinates

    temperature: int
        cell's current temperature

    wind: str
        cell's wind direction

    pollution: float
        cell's pollution amount from 0-no pollution 1-polluted

    clouds: float
        cell's cloud coverage 0-clear sky 1-heavy clouds

    """

    state_map = {
        "S": Sea(),
        "I": Ice(),
        "F": Forest(),
        "D": Desert(),
        "M": Mountain(),
        "C": City(),
    }

    def __init__(self, coordinate: tuple[int, int], cell_type: str):
        self._coordinates = coordinate
        self.init_weather(self.state_map[cell_type])

    @property
    def neighbors(self):
        """returns Neighborhood instance of current cell"""
        return self._neighbor

    def neighbors_init(self, grid: Grid):
        self._neighbor = Neighborhood(self, grid)

    @property
    def x_cord(self) -> int:
        """returns x coordinate"""
        return self._coordinates[0]

    @property
    def y_cord(self) -> int:
        """returns y coordinate"""
        return self._coordinates[1]

    @property
    def temperature(self) -> int:
        return self._temperature

    @temperature.setter
    def temperature(self, val: int):
        self._temperature = val

    @property
    def wind(self) -> str:
        return self._wind

    @wind.setter
    def wind(self, val: str):
        self._wind = val

    @property
    def pollution(self) -> float:
        return self._pollution

    @pollution.setter
    def pollution(self, val: float):
        self._pollution = val

    @property
    def clouds(self) -> float:
        return self._clouds

    @clouds.setter
    def clouds(self, val: float):
        self._clouds = val

    def init_weather(self, concrete_state):
        self.transition(concrete_state)
        self.temperature = randint(
            self.state.temp_range["min"], self.state.temp_range["max"]
        )

    def transition(self, state):
        self._state = state
        self._state.cell = self

    @property
    def state(self) -> Sea | Ice | Forest | Desert | City | Mountain:
        return self._state


if __name__ == "__main__":
    global g_world_diemention
    g_world_diemention = WorldDiementions(
        cell_num_length=40, cell_num_width=20, cell_size=20
    )
    glob_warm = GlobalWarmingModel()
