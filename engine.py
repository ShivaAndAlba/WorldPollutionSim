import tkinter as tk
from dataclasses import dataclass

import cell_state_machine as csm
from worldMap import worldMap


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

    def model_init(self, world_dimention):
        self.world_dimention = world_dimention

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
        self.grid = Grid(self.world_dimention, self.canvas)
        self.grid.insert_cell()
        self.root.mainloop()


# TODO: rewrite this class mmore organized
class Grid:
    """two dimenional array of cellls
    manages creation and updates of each cell state"""

    def __init__(self, dimentions: WorldDiementions, canvas: tk.Canvas):
        self.canvas = canvas
        self.dimentions = dimentions
        self._grid = [
            [csm.Cell((x, y), worldMap[x][y]) for y in range(dimentions.length)]
            for x in range(dimentions.width)
        ]

        for y, x in range(dimentions.width), range(dimentions.length):
            self.cell_at(y, x).neighbors_init()

    def cell_at(self, point_y, point_x):
        return self._grid[point_y][point_x]

    def insert_cell(self):
        """create and insert cells to canvas"""
        cell_size = self.dimentions.cell_size

        for point_x, point_y in range(self.dimentions.width), range(
            self.dimentions.length
        ):
            cell = self.cell_at(point_y, point_x)
            cell.canvas.id = self.canvas.create_rectangle(
                point_x * cell_size,
                point_y * cell_size,
                (point_x + 1) * cell_size,
                (point_y + 1) * cell_size,
                fill=cell.canvas.cell_color(),
            )

            # TODO: change what text is shown from app window
            cell.canvas.text = self.canvas.create_text(
                (point_x + 0.5) * self.dimentions.cell_size,
                (point_y + 0.5) * self.dimentions.cell_size,
                text=str(cell.temperature),
            )


if __name__ == "__main__":
    world_diemention = WorldDiementions(length=40, width=20, cell_size=20)
    glob_warm = GlobalWarmingModel()
    glob_warm.model_init(world_diemention)
