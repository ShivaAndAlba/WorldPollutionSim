import tkinter as tk
from dataclasses import dataclass

import cell_state_machine as csm
import worldMap


@dataclass
class WorldDiementions:
    length: int
    width: int
    cell_size: int

    def get_cell_length(self):
        """returns cell length"""
        return self.length * self.cell_size

    def get_cell_width(self):
        """returns cell width"""
        return self.width * self.cell_size


class GlobalWarmingModel:
    """singelton class to handle all model functionality"""

    def __new__(cls):
        if not hasattr(cls, "instance"):
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
        self.canvas = tk.Canvas(
            self.root,
            height=self.world_dimention.get_cell_width(),
            width=self.world_dimention.get_cell_length(),
        )
        self.canvas.pack()
        self.insert_cell()
        self.root.mainloop()

    def insert_cell(self):
        """create and insert cells to canvas"""
        for point_x, point_y in range(self.world_dimention.width), range(
            self.world_dimention.length
        ):
            cell = self.grid.cell_at(point_y, point_x)
            cell.set_canvas_id(
                self.canvas.create_rectangle(
                    point_x * self.world_dimention.cell_size,
                    point_y * self.world_dimention.cell_size,
                    (point_x + 1) * self.world_dimention.cell_size,
                    (point_y + 1) * self.world_dimention.cell_size,
                    fill=cell.get_color(),
                )
            )
            cell.set_canvas_text(
                self.canvas.create_text(
                    (point_x + 0.5) * worldDiemention.cell_size,
                    (point_y + 0.5) * worldDiemention.cell_size,
                    text=str(cell.get_temprature()),
                )
            )


# TODO: rewrite this class mmore organized
class Grid:
    """two dimenional array of cellls
    manages creation and updates of each cell state"""

    def __init__(self, dimentions: WorldDiementions) -> None:
        self.dimentions = dimentions
        # TODO: solve state init here, who is responsible to create cell types
        self._grid = [
            [csm.Cell((y, x)) for x in range(dimentions.length)]
            for y in range(dimentions.width)
        ]

        for y, x in range(dimentions.width), range(dimentions.length):
            self.cell_at(y, x).neighbors_init()

    def cell_at(self, point_y, point_x):
        return self._grid[point_y][point_x]
