from __future__ import annotations

from tkinter import Tk, BOTH, Canvas


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


def main():
    win = Window(800, 600)
    line = Line(Point(100, 100), Point(200, 200))
    win.draw_line(line)
    win.wait_for_close()


if __name__ == "__main__":
    main()
