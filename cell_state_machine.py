from abc import ABC, abstractmethod
from engine import Grid


class Cell:
    """
    cell class describes cell's coordinates, neighbors and state
    """

    _state = None

    def __init__(self, state: State, point: tuple) -> None:
        self._point = point
        self.set_state(state)

    @property
    def neighbors(self):
        """returns Neighborhood instance of current cell"""
        return self._neighbor

    @neighbors.setter
    def neighbors(self):
        self._neighbor = Neighborhood(self)

    @property
    def x_cord(self) -> int:
        """returns x coordinate"""
        return self._point[0]

    @property
    def y_cord(self) -> int:
        """returns y coordinate"""
        return self._point[1]

    def set_state(self, state: State):
        self._state = state
        self._state.cell = self

    def state(self) -> State:
        return self._state
# TODO: create methods to execute cells functionality


class State(ABS):
    @property
    def cell(self) -> Cell:
        return self._cell

    @cell.setter
    def cell(self, cell: Cell):
        self._cell = cell

# TODO: add abs methods of cell
    @abstractmethod
    def ab_method(self):
        pass

# TODO: create class of each state implementing states abs methods


class Neighborhood(Grid):
    """handels all cell's neighbors data"""

    def __init__(self, cell: Cell):
        self.north(cell)
        self.south(cell)
        self.west(cell)
        self.east(cell)

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

    @north.setter
    def north(self, cell: Cell):
        if self.cell_north_bound(cell):
            y_cord = self.dimentions.width - 1
        else:
            y_cord = cell.y_cord-1

        self._north =\
            self.cell_at(y_cord, cell.x_cord)

    @property
    def south(self):
        return self._south

    @south.setter
    def south(self, cell: Cell):
        if self.cell_south_bound(cell):
            y_cord = 0
        else:
            y_cord = cell.y_cord+1

        self._south =\
            self.cell_at(y_cord, cell.x_cord)

    @property
    def west(self):
        return self._west

    @west.setter
    def west(self, cell: Cell):
        if self.cell_west_bound(cell):
            x_cord = self.dimentions.length - 1
        else:
            x_cord = cell.x_cord-1

        self._west =\
            self.cell_at(cell.y_cord, x_cord)

    @property
    def east(self):
        return self._east

    @east.setter
    def east(self, cell: Cell):
        if self.cell_east_bound(cell):
            x_cord = 0
        else:
            x_cord = cell.x_cord+1

        self._east =\
            self.cell_at(x_cord, cell.y_cord)
