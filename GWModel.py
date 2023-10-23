from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from functools import partial
from random import randint
from time import sleep

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
        self.blocked = False
        self.sim_iter = 300

        """creates gui via tkinter"""
        self.root = tk.Tk()
        self.title = self.root.title("Air Polution Model - Ex. 11")

        # # label
        # self.label = tk.Label(self.root)
        # self.label.pack()

        # canvas frame
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=0, column=1)
        self._canvas = tk.Canvas(
            self.canvas_frame,
            height=g_world_diemention.width,
            width=g_world_diemention.length,
        )
        self._canvas.pack()

        # buttons frame
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.grid(row=0, column=0, columnspan=1)

        self.run_btn = tk.Button(
            self.btn_frame, text="Run", command=self.sim_run, width=7
        ).pack(expand=True)
        self.stop_btn = tk.Button(
            self.btn_frame, text="Stop", command=self.sim_stop, width=7
        ).pack(expand=True)
        self.reset_btn = tk.Button(
            self.btn_frame, text="Reset", command=self.sim_reset, width=7
        ).pack(expand=True)
        self.quit_btn = tk.Button(
            self.btn_frame, text="Quit", command=self.root.destroy, width=7
        ).pack(expand=True)

        # entry frame
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(row=1, column=0, columnspan=1, rowspan=1)

        self.entry_label = tk.Label(
            self.entry_frame, text="Set # itterations(Default:300)"
        )
        self.entry_box = tk.Entry(self.entry_frame, width=11)
        self.entry_box.insert(0, str(self.sim_iter))
        self.entry_box.pack()

        self.set_itter_callable = partial(self.set_itteration, self.entry_box)
        self.set_btn = tk.Button(
            self.entry_frame, text="Set", command=self.set_itter_callable, width=7
        ).pack(expand=True)

    def set_itteration(self):
        self.sim_iter = int(self.entry_box.get())

    def sim_run(self):
        self.blocked = False

        for _ in range(self.sim_iter):
            # calculate next generation
            self.calculate_next_gen()
            # transition every cell to new state
            self.transition_cells()
            # update canvas
            # calculate average and store
            # chech if sim_run  is false then exit
            if self.blocked:
                break
            # wait for 50 ms
            sleep(0.1)
        pass

    def sim_reset(self):
        self.sim_iter = 300

    def sim_stop(self):
        self.blocked = True

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

    def calculate_next_gen(self):
        for y in range(g_world_diemention.cell_num_width):
            for x in range(g_world_diemention.cell_num_length):
                print("itr:", x, y)
                self.grid.cell_at(y, x).state.effect()

    def transition_cells(self):
        for y in range(g_world_diemention.cell_num_width):
            for x in range(g_world_diemention.cell_num_length):
                print("transition:", x, y)
                self.grid.cell_at(y, x).transition_to_next_gen()


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
        for x in range(g_world_diemention.cell_num_length):
            for y in range(g_world_diemention.cell_num_width):
                self.cell_at(y, x).neighbors_init(self)

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

    def mean_of(self) -> dict:
        temp_mean = np.mean([temp.temperature for temp in self.everyone().values()])
        return {"temp_mean": temp_mean}


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
        self.transition_queue = []
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

    def transition_enqueue(self, state: Sea | Ice | Forest | Desert | City | Mountain):
        self.transition_queue.append(state)

    def transition_to_next_gen(self):
        if self.transition_queue:
            state = self.transition_queue.pop()
            self.transition(state)

    def transition(self, state: Sea | Ice | Forest | Desert | City | Mountain):
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
