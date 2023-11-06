from __future__ import annotations

import tkinter as tk
from functools import partial

import cell_automata as ca
from worldMap import g_world_diemention, worldMap


class GWModel:
    """
    Creates gui, cells and relations of cells, handle calculations
    ...
    Attributes:
    ----------
    blocked: int
        variable for stoping the siulation

    itter: int
        counter of itterations

    grid: Grid
        handle for a cell logic and graphic

    properties:
    ----------
        canvas: int
            handle for a container of rectangles witch represent cells

    """

    def __init__(self):
        self.init_gui()
        self.init_grid()
        self.tk_mainloop()

    def init_grid(self):
        self.grid = Grid(self.canvas)

    def init_gui(self):
        self.blocked = None
        self.sim_iter = 20

        self.root = tk.Tk()
        self.title = self.root.title("Air Polution Model - Ex. 11")

        # canvas frame
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=0, column=1)
        self.canvas = tk.Canvas(
            self.canvas_frame,
            height=g_world_diemention.width,
            width=g_world_diemention.length,
        )
        self.canvas.pack()

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
            self.entry_frame, text="Set # itterations(Default:20)"
        )
        self.entry_box = tk.Entry(self.entry_frame, width=11)
        self.entry_box.insert(0, str(self.sim_iter))
        self.entry_box.pack()

        self.set_itter_callable = partial(self.set_itteration)
        self.set_btn = tk.Button(
            self.entry_frame, text="Set", command=self.set_itter_callable, width=7
        ).pack(expand=True)

    def sim_run(self):
        self.run_iteration()

    def sim_stop(self):
        self.root.after_cancel(self.blocked)

    def set_itteration(self):
        self.sim_iter = int(self.entry_box.get())

    def sim_reset(self):
        self.grid.reset()

    def tk_mainloop(self):
        self.root.mainloop()

    def run_iteration(self):
        # calculate next generation
        self.calculate_next_gen()
        # transition every cell to new state ,
        # update temp text and update cell color
        self.update_cells()
        self.root.update_idletasks()
        # calculate average and store
        if self.sim_iter:
            self.sim_iter -= 1
            self.blocked = self.root.after(100, self.run_iteration)
        else:
            self.sim_iter = 20
            self.sim_stop()

    def calculate_next_gen(self):
        for y in range(g_world_diemention.cell_num_width):
            for x in range(g_world_diemention.cell_num_length):
                self.grid.cell_obj_at(y, x).state.effect()

    def update_cells(self):
        for y in range(g_world_diemention.cell_num_width):
            for x in range(g_world_diemention.cell_num_length):
                cell = self.grid.cell_obj_at(y, x)
                cell.transition_to_next_gen()
                cell.update_cell_color()
                cell.update_cell_text()

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, canvas: tk.Canvas):
        self._canvas = canvas


class Grid:
    """
    creates object matrices of cell and canvas cells, establish relation between cell
    objects(neighbors).
    container of cell object matrix and cell canvas object with access to indevidual
    object via coordinates.
    ...
    attributes:
    ----------
    canvas: int
        handle of a frame for graphic cells

    cell_obj_matx: list[list[Cell]]
        2d array of Cell objects(each Cell is a state machine)

    cell_canvas_matx: list[list[CellCavas]]
        2d array of CellCanvas objects(each CellCanvas coresponds to the
        Cell object at the same coordinates, represent Cell object's graphic represention)

    """

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.cell_obj_matx: list[list[ca.Cell]]
        self.init_cell_grid()
        self.init_cell_canvas()
        self.init_cell_neighbors()

    def init_cell_grid(self):
        self.cell_obj_matx = [
            [
                ca.Cell((x, y), worldMap[y][x])
                for x in range(g_world_diemention.cell_num_length)
            ]
            for y in range(g_world_diemention.cell_num_width)
        ]

    def init_cell_canvas(self):
        self.cell_canvas_matx = [
            [
                ca.CellCanvas(
                    self.canvas, self.cell_obj_at(y, x), g_world_diemention.cell_size
                )
                for x in range(g_world_diemention.cell_num_length)
            ]
            for y in range(g_world_diemention.cell_num_width)
        ]

    def init_cell_neighbors(self):
        for x in range(g_world_diemention.cell_num_length):
            for y in range(g_world_diemention.cell_num_width):
                self.cell_obj_at(y, x).neighbors_init(self)

    def reset(self):
        for y in range(g_world_diemention.cell_num_width):
            for x in range(g_world_diemention.cell_num_length):
                self.cell_obj_at(y, x).init_weather(worldMap[y][x])
                self.cell_canvas_at(y, x).update_cell_color()
                self.cell_canvas_at(y, x).update_text()

    def cell_obj_at(self, point_y, point_x):
        return self.cell_obj_matx[point_y][point_x]

    def cell_canvas_at(self, point_y, point_x):
        return self.cell_canvas_matx[point_y][point_x]


if __name__ == "__main__":
    glob_warm = GWModel()
