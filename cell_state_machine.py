import tkinter as tk
from abc import ABC, abstractmethod
from random import randint

import numpy as np

from engine import Grid


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

    _state = None
    state_map = {"S": Sea, "I": Ice, "F": Forest, "D": Desert, "M": Mountain, "C": City}

    def __init__(self, point: tuple, cell_type: str):
        state = self.state_map[cell_type]
        self._coordinates = point
        self.init_weather(state)
        self.transition(state)

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, id: int):
        self._canvas = CellCanvas(id)

    @property
    def neighbors(self):
        """returns Neighborhood instance of current cell"""
        return self._neighbor

    def neighbors_init(self):
        self._neighbor = Neighborhood(self)

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
        return self.temperature

    @temperature.setter
    def temperature(self, val: int):
        self.temperature = val

    @property
    def wind(self) -> str:
        return self.wind

    @wind.setter
    def wind(self, val: str):
        self.wind = val

    @property
    def pollution(self) -> float:
        return self.pollution

    @pollution.setter
    def pollution(self, val: float):
        self.pollution = val

    @property
    def clouds(self) -> float:
        return self.clouds

    @clouds.setter
    def clouds(self, val: float):
        self.clouds = val

    def init_weather(self, state: State):
        self.temperature = randint(state.temp_range["min"], state.temp_range["max"])

    def transition(self, state: State):
        self._state = state
        self._state.cell = self

    def state(self) -> State:
        return self._state


class State(ABC):
    """
    Interface for cell's state.
    Cell can change states according to the weather in state state.
    state change is determind by cell's neighbors from N,S,W,E
    state affect diffrently on other states
    states are described with classes Sea,Ice,Forest,Desert,City
    State change funcion:
        Sea -> Ice: if temerature drops below 0
        Ice -> Sea: if temperature goes above 0
        Forest -> Desert: if no clouds, temperature above 40
        Desert -> Forest: if clouds and temperature below 40
        City -> Desert: if temperature above 40 and pollution is max
    cities create pollution witch is scattered with the wind.
    pollution raises temperature.
    clouds are created over forests and sea, and sometimes
    drops rain witch lowers temperature and lowers pollution.
    """

    @property
    def cell(self) -> Cell:
        return self._cell

    @cell.setter
    def cell(self, cell: Cell):
        self._cell = cell

    @abstractmethod
    def effect(self):
        pass

    def temp_effect(self, factors: dict, temp_range: dict):
        mean_temp = self.cell.neighbors.mean_of("temperature")
        self.cell.temperature = (
            np.mean([self.cell.temperature, mean_temp]) * factors["temp_fact"]
        )

        if self.cell.temperature > temp_range["max"]:
            self.cell.temperature = temp_range["max"]
        elif self.cell.temperature < temp_range["min"]:
            self.cell.temperature = temp_range["min"]


class Sea(State):
    state_color = "#1273de"
    temp_range = {"min": 0, "max": 35}
    factors = {"temp_fact": 0.8}

    def effect(self):
        self.temp_effect(self.factors, self.temp_range)
        if self.cell.temperature == self.temp_range["min"]:
            self.cell.transition(Ice)


class Ice(State):
    state_color = "#ffffff"
    temp_range = {"min": -20, "max": 0}
    factors = {"temp": 0.6}

    def effect(self):
        self.temp_effect(self.factors, self.temp_range)
        if self.cell.temperature == self.temp_range["max"]:
            self.cell.transition(Sea)


class Forest(State):
    state_color = "#7ed321"
    temp_range = {"min": 0, "max": 30}
    factors = {"temp": 0.8}

    def effect(self):
        self.temp_effect(self.temp_range, self.factors)
        if self.cell.temperature == self.temp_range["max"]:
            self.cell.transition(Desert)
        elif self.cell.temperature == self.temp_range["min"]:
            self.cell.transition(Ice)


class Desert(State):
    state_color = "#f8e71c"
    temp_range = {"min": 30, "max": 50}
    factors = {"temp": 0.4}

    def effect(self):
        self.temp_effect(self.temp_range, self.factors)
        if self.cell.temperature == self.temp_range["min"]:
            self.cell.transition(Forest)


class City(State):
    state_color = "#9b9b9b"
    temp_range = {"min": 0, "max": 40}
    factors = {"temp": 0.4}

    def effect(self):
        self.temp_effect(self.temp_range, self.factors)
        if self.cell.temperature == self.temp_range["max"]:
            self.cell.transition(Desert)


class Mountain(State):
    state_color = "#1976d2"
    temp_range = {"min": -20, "max": 20}
    factors = {"temp": 0.4}

    def effect(self):
        self.temp_effect(self.temp_range, self.factors)


class Neighborhood(Grid):
    """handels all cell's neighbors data"""

    def __init__(self, cell: Cell):
        self.set_north(cell)
        self.set_south(cell)
        self.set_west(cell)
        self.set_east(cell)

    def cell_north_bound(self, cell: Cell):
        """checks if cell is at the top of the grid"""
        return cell.y_cord == 0

    def cell_south_bound(self, cell: Cell):
        """check if cell is at the bottom of the grid"""
        return cell.y_cord > self.dimentions.width - 2

    def cell_west_bound(self, cell: Cell):
        """check if cell is at the rightest of the grid"""
        return cell.x_cord == 0

    def cell_east_bound(self, cell: Cell):
        """check if cell is the leftest of the grid"""
        return cell.x_cord > self.dimentions.length - 2

    @property
    def north(self):
        return self._north

    def set_north(self, cell: Cell):
        if self.cell_north_bound(cell):
            y_cord = self.dimentions.width - 1
        else:
            y_cord = cell.y_cord - 1

        self._north = self.cell_at(y_cord, cell.x_cord)

    @property
    def south(self):
        return self._south

    def set_south(self, cell: Cell):
        if self.cell_south_bound(cell):
            y_cord = 0
        else:
            y_cord = cell.y_cord + 1

        self._south = self.cell_at(y_cord, cell.x_cord)

    @property
    def west(self):
        return self._west

    def set_west(self, cell: Cell):
        if self.cell_west_bound(cell):
            x_cord = self.dimentions.length - 1
        else:
            x_cord = cell.x_cord - 1

        self._west = self.cell_at(cell.y_cord, x_cord)

    @property
    def east(self):
        return self._east

    def set_east(self, cell: Cell):
        if self.cell_east_bound(cell):
            x_cord = 0
        else:
            x_cord = cell.x_cord + 1

        self._east = self.cell_at(x_cord, cell.y_cord)

    def everyone(self) -> dict[str, Cell]:
        return {"N": self.north, "S": self.south, "W": self.west, "E": self.east}

    def mean_of(self, prop: str) -> int:
        return np.mean([temp.__dict__[prop] for temp in self.everyone().values()])


class CellCanvas(Cell):
    def cell_color(self) -> str:
        return self.state.state_color

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def text(self) -> int:
        return self._text

    @text.setter
    def text(self, text: int):
        self._text = text
