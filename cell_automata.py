from __future__ import annotations

import tkinter as tk
from random import choice, randint, random, uniform

import numpy as np

import GWModel as gw
from states import City, Desert, Forest, Ice, Mountain, Sea


class CellCanvas:
    """
    create and handle cell's graphic operations
    ...
    Attributes:
    ----------
    canvas: int
        handle of a frame for graphic cells

    cell_size: int
        cell size detemined by world map

    cell: Cell
        handle to cell object which represented by CellCanvas object

    cell_canvas: int
        handle of a rectangle created by tkinter

    cell_text: int
        handle of a text inside the cell_canvas

    """

    def __init__(self, canvas: tk.Canvas, cell: Cell, cell_size: int):
        self.canvas = canvas
        self.cell_size = cell_size
        self.cell = cell
        self.cell.cell_canvas = self
        self.cell_canvas = self.draw_cell()
        self.cell_text = self.init_text()

    def draw_cell(self):
        return self.canvas.create_rectangle(
            self.cell.x_cord * self.cell_size,
            self.cell.y_cord * self.cell_size,
            (self.cell.x_cord + 1) * self.cell_size,
            (self.cell.y_cord + 1) * self.cell_size,
            fill=self.cell_color(),
        )

    def cell_color(self) -> str:
        return self.cell.state.state_color

    def update_cell_color(self):
        self.canvas.itemconfig(self.cell_canvas, fill=self.cell_color())

    def init_text(self):
        return self.canvas.create_text(
            (self.cell.x_cord + 0.5) * self.cell_size,
            (self.cell.y_cord + 0.5) * self.cell_size,
            text=str(self.cell.temperature),
        )

    def update_text(self):
        self.canvas.itemconfigure(self.cell_text, text=str(int(self.cell.temperature)))


class Neighborhood:
    """
    connects cell object to its adjacent cells(imidiate neighborhood - cells from the
    north, south, west, east), cells at the boudry of the grid conneted to opposing
    side(round robin)
    ...
    Attributes:
    ----------
    grid: Grid
        handle for a cell logic and graphic

    Properties:
    ----------
    north, south, west, east: Cell
        cell at coresponding directions

    """

    def __init__(self, cell: Cell, grid: gw.Grid):
        self.grid = grid
        self.set_north(cell)
        self.set_south(cell)
        self.set_west(cell)
        self.set_east(cell)

    def cell_north_bound(self, cell: Cell) -> bool:
        """checks if cell is at the top of the grid"""
        return cell.y_cord == 0

    def cell_south_bound(self, cell: Cell) -> bool:
        """check if cell is at the bottom of the grid"""
        return cell.y_cord > gw.g_world_diemention.cell_num_width - 2

    def cell_west_bound(self, cell: Cell) -> bool:
        """check if cell is at the rightest of the grid"""
        return cell.x_cord == 0

    def cell_east_bound(self, cell: Cell) -> bool:
        """check if cell is the leftest of the grid"""
        return cell.x_cord > gw.g_world_diemention.cell_num_length - 2

    @property
    def north(self) -> Cell:
        return self._north

    def set_north(self, cell: Cell):
        if self.cell_north_bound(cell):
            y_cord = gw.g_world_diemention.cell_num_width - 1
        else:
            y_cord = cell.y_cord - 1

        self._north = self.grid.cell_obj_at(y_cord, cell.x_cord)

    @property
    def south(self) -> Cell:
        return self._south

    def set_south(self, cell: Cell):
        if self.cell_south_bound(cell):
            y_cord = 0
        else:
            y_cord = cell.y_cord + 1

        self._south = self.grid.cell_obj_at(y_cord, cell.x_cord)

    @property
    def west(self) -> Cell:
        return self._west

    def set_west(self, cell: Cell):
        if self.cell_west_bound(cell):
            x_cord = gw.g_world_diemention.cell_num_length - 1
        else:
            x_cord = cell.x_cord - 1

        self._west = self.grid.cell_obj_at(cell.y_cord, x_cord)

    @property
    def east(self) -> Cell:
        return self._east

    def set_east(self, cell: Cell):
        if self.cell_east_bound(cell):
            x_cord = 0
        else:
            x_cord = cell.x_cord + 1

        self._east = self.grid.cell_obj_at(cell.y_cord, x_cord)

    def everyone(self) -> dict[str, Cell]:
        return {"N": self.north, "S": self.south, "W": self.west, "E": self.east}

    def mean_of(self) -> dict:
        temp_mean = np.mean(
            [neighbor.temperature for neighbor in self.everyone().values()]
        )
        wind_neighbors = [neighbor.wind for neighbor in self.everyone().values()]
        wind_mean = max(wind_neighbors, key=wind_neighbors.count)
        return {"temp_mean": temp_mean, "wind_mean": wind_mean}


class Cell:
    """
    A class describing single cell in cellular automata.
    Cells are state machines that change states according to cells weather.
    ...
    Attributes
    ---------
    state_map: dict[str, State]
        dictionary with instantiated states

    transition_queue: list
        queue of States for transtion after iteration calculation is done

    neighbors : Neighborhood
        cell's neighbors from N,S,W,E

    properties:
    ----------
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

    def __init__(self, coordinate: tuple[int, int], cell_type: str):
        self.state_map = {
            "S": Sea(),
            "I": Ice(),
            "F": Forest(),
            "D": Desert(),
            "M": Mountain(),
            "C": City(),
        }

        self.transition_queue = []
        self._coordinates = coordinate
        self.init_weather(cell_type)

    def update_cell_color(self):
        self.cell_canvas.update_cell_color()

    def update_cell_text(self):
        self.cell_canvas.update_text()

    def init_weather(self, cell_type: str):
        self.transition(self.state_map[cell_type])
        self.temperature = randint(
            self.state.temp_range["min"], self.state.temp_range["max"]
        )
        self.wind = choice(["N", "S", "W", "E"])
        self.pollution = 0.7 if cell_type == "C" else uniform(0, 0.4)
        self.clouds = random()

    def transition_enqueue(self, state: Sea | Ice | Forest | Desert | City | Mountain):
        self.transition_queue.append(state)

    def transition_to_next_gen(self):
        if self.transition_queue:
            self.transition(self.transition_queue.pop())

    def transition(self, state: Sea | Ice | Forest | Desert | City | Mountain):
        self._state = state
        self._state.cell = self

    @property
    def neighbors(self):
        """returns Neighborhood instance of current cell"""
        return self._neighbor

    def neighbors_init(self, grid: gw.Grid):
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

    @property
    def cell_canvas(self) -> CellCanvas:
        return self._cell_canvas

    @cell_canvas.setter
    def cell_canvas(self, cell_canvas_inst: CellCanvas):
        self._cell_canvas = cell_canvas_inst

    @property
    def state(self) -> Sea | Ice | Forest | Desert | City | Mountain:
        return self._state
