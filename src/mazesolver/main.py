from __future__ import annotations

from tkinter import Tk, BOTH, Canvas

import enum


class Sides(enum.Flag):
    NONE = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 4
    RIGHT = 8
    ALL = TOP | BOTTOM | LEFT | RIGHT


class Window:
    def __init__(
        self, width: int = 1280, height: int = 720, title: str = "Maze Solver"
    ):
        self.root = Tk()
        self.root.title(title)
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def draw_line(self, line: Line, color: str = "black"):
        line.draw(self.canvas, color)

    def close(self):
        self.running = False


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, color: str = "black"):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=color
        )

class Cell:
    def __init__(self, window: Window, topleft: Point, bottomright: Point, walls: Sides = Sides.ALL):
        self.window = window
        self.topleft = topleft
        self.bottomright = bottomright
        self.walls = walls

    @property
    def bottomleft(self) -> Point:
        return Point(self.topleft.x, self.bottomright.y)

    @property
    def topright(self) -> Point:
        return Point(self.bottomright.x, self.topleft.y)

    @property
    def center(self) -> Point:
        return Point((self.topleft.x + self.bottomright.x) / 2, (self.topleft.y + self.bottomright.y) / 2)

    def draw(self):
        if self.walls & Sides.TOP:
            self.window.draw_line(Line(self.topleft, self.topright))
        if self.walls & Sides.BOTTOM:
            self.window.draw_line(Line(self.bottomleft, self.bottomright))
        if self.walls & Sides.LEFT:
            self.window.draw_line(Line(self.topleft, self.bottomleft))
        if self.walls & Sides.RIGHT:
            self.window.draw_line(Line(self.topright, self.bottomright))

    def draw_move(self, to_cell: Cell, undo: bool = False):
        color = "red" if not undo else "gray"
        self.window.draw_line(Line(self.center, to_cell.center), color)

def main():
    win = Window(800, 600)
    line = Line(Point(100, 100), Point(200, 200))
    win.draw_line(line)
    cell1 = Cell(win, Point(100, 100), Point(200, 200))
    cell2 = Cell(win, Point(300, 100), Point(400, 200))
    cell1.draw()
    cell2.draw()
    cell1.draw_move(cell2)
    win.wait_for_close()


if __name__ == "__main__":
    main()
