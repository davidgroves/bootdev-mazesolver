from __future__ import annotations

from tkinter import Tk, BOTH, Canvas

import enum
import time
import random

SLEEP_TIME = 0.05


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
    def __init__(
        self,
        window: Window,
        topleft: Point,
        bottomright: Point,
        walls: Sides = Sides.ALL,
        visited: bool = False,
    ):
        self.window = window
        self.topleft = topleft
        self.bottomright = bottomright
        self.walls = walls
        self.visited = visited

    @property
    def bottomleft(self) -> Point:
        return Point(self.topleft.x, self.bottomright.y)

    @property
    def topright(self) -> Point:
        return Point(self.bottomright.x, self.topleft.y)

    @property
    def center(self) -> Point:
        return Point(
            (self.topleft.x + self.bottomright.x) / 2,
            (self.topleft.y + self.bottomright.y) / 2,
        )

    @property
    def left_wall(self) -> bool:
        return self.walls & Sides.LEFT

    @property
    def right_wall(self) -> bool:
        return self.walls & Sides.RIGHT

    @property
    def top_wall(self) -> bool:
        return self.walls & Sides.TOP

    @property
    def bottom_wall(self) -> bool:
        return self.walls & Sides.BOTTOM

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


class Maze:
    def __init__(
        self,
        x_offset: int,
        y_offset: int,
        rows: int,
        cols: int,
        cell_width: int,
        cell_height: int,
        window: Window = None,
        seed: int = None,
    ):
        if seed is not None:
            random.seed(seed)
        self.topleft = Point(x_offset, y_offset)
        self.rows = rows
        self.cols = cols
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.window = window
        self.create_cells()

    def create_cells(self):
        self.cells = [
            [
                Cell(
                    self.window,
                    Point(
                        x * self.cell_width + self.topleft.x,
                        y * self.cell_height + self.topleft.y,
                    ),
                    Point(
                        (x + 1) * self.cell_width + self.topleft.x,
                        (y + 1) * self.cell_height + self.topleft.y,
                    ),
                )
                for x in range(self.cols)
            ]
            for y in range(self.rows)
        ]

    def draw_cell(self, x: int, y: int):
        self.cells[y][x].draw()
        self.animate()

    def animate(self):
        self.window.redraw()
        time.sleep(SLEEP_TIME)

    def break_entrance_and_exit(self, x: int, y: int):
        if x == 0 and y == 0:
            self.cells[y][x].walls &= ~Sides.LEFT
        elif x == self.cols - 1 and y == self.rows - 1:
            self.cells[y][x].walls &= ~Sides.RIGHT
        elif x == 0:
            self.cells[y][x].walls &= ~Sides.TOP
        elif x == self.cols - 1:
            self.cells[y][x].walls &= ~Sides.BOTTOM
        else:
            raise ValueError("Cannot break entrance and exit for non-edge cell")

    def break_walls(self, x: int, y: int):
        self.cells[y][x].visited = True
        while True:
            possible_moves = []

            # Left neighbor
            if x > 0 and not self.cells[y][x - 1].visited:
                possible_moves.append((x - 1, y))
            # Right neighbor
            if x < self.cols - 1 and not self.cells[y][x + 1].visited:
                possible_moves.append((x + 1, y))
            # Top neighbor
            if y > 0 and not self.cells[y - 1][x].visited:
                possible_moves.append((x, y - 1))
            # Bottom neighbor
            if y < self.rows - 1 and not self.cells[y + 1][x].visited:
                possible_moves.append((x, y + 1))

            if not possible_moves:
                self.draw_cell(x, y)
                return

            # Choose random direction
            next_x, next_y = random.choice(possible_moves)

            # Break walls between current and chosen cell
            if next_x < x:  # Moving left
                self.cells[y][x].walls &= ~Sides.LEFT
                self.cells[next_y][next_x].walls &= ~Sides.RIGHT
            elif next_x > x:  # Moving right
                self.cells[y][x].walls &= ~Sides.RIGHT
                self.cells[next_y][next_x].walls &= ~Sides.LEFT
            elif next_y < y:  # Moving up
                self.cells[y][x].walls &= ~Sides.TOP
                self.cells[next_y][next_x].walls &= ~Sides.BOTTOM
            else:  # Moving down
                self.cells[y][x].walls &= ~Sides.BOTTOM
                self.cells[next_y][next_x].walls &= ~Sides.TOP

            # Recursively visit next cell
            self.break_walls(next_x, next_y)

    def reset_visited_cells(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def solve_r(self, x: int, y: int) -> bool:
        self.animate()
        self.cells[y][x].visited = True
        print(f"Solving cell {x}, {y}")

        if x == self.cols - 1 and y == self.rows - 1:
            print(f"Reached end cell {x}, {y}")
            return True

        print(f"Left: {self.cells[y][x].left_wall} {bool(self.cells[y][x].left_wall)}")
        print(f"Right: {self.cells[y][x].right_wall} {bool(self.cells[y][x].right_wall)}")
        print(f"Top: {self.cells[y][x].top_wall} {bool(self.cells[y][x].top_wall)}")
        print(f"Bottom: {self.cells[y][x].bottom_wall} {bool(self.cells[y][x].bottom_wall)}")
        # Try each direction
        # Left
        if (
            x > 0
            and not self.cells[y][x].left_wall
            and not self.cells[y][x - 1].visited
        ):
            print(f"Moving left from {x}, {y} to {x-1}, {y}")
            self.cells[y][x].draw_move(self.cells[y][x - 1])
            if self.solve_r(x - 1, y):
                return True
            self.cells[y][x].draw_move(self.cells[y][x - 1], undo=True)
            print(f"Backtracking from {x-1}, {y} to {x}, {y}")

        # Right
        if (
            x < self.cols - 1
            and not self.cells[y][x].right_wall
            and not self.cells[y][x + 1].visited
        ):
            print(f"Moving right from {x}, {y} to {x+1}, {y}")
            self.cells[y][x].draw_move(self.cells[y][x + 1])
            if self.solve_r(x + 1, y):
                return True
            self.cells[y][x].draw_move(self.cells[y][x + 1], undo=True)
            print(f"Backtracking from {x+1}, {y} to {x}, {y}")

        # Up
        if (
            y > 0
            and not self.cells[y][x].top_wall
            and not self.cells[y - 1][x].visited
        ):
            print(f"Moving up from {x}, {y} to {x}, {y-1}")
            self.cells[y][x].draw_move(self.cells[y - 1][x])
            if self.solve_r(x, y - 1):
                return True
            self.cells[y][x].draw_move(self.cells[y - 1][x], undo=True)
            print(f"Backtracking from {x}, {y-1} to {x}, {y}")

        # Down
        if (
            y < self.rows - 1
            and not self.cells[y][x].bottom_wall
            and not self.cells[y + 1][x].visited
        ):
            print(f"Moving down from {x}, {y} to {x}, {y+1}")
            self.cells[y][x].draw_move(self.cells[y + 1][x])
            if self.solve_r(x, y + 1):
                return True
            self.cells[y][x].draw_move(self.cells[y + 1][x], undo=True)
            print(f"Backtracking from {x}, {y+1} to {x}, {y}")

        # Reset visited state when backtracking
        self.cells[y][x].visited = False
        print(f"No solution found from {x}, {y}")
        return False


def main():
    win = Window(800, 600)

    rows = cols = 6
    maze = Maze(
        x_offset=50,
        y_offset=50,
        rows=rows,
        cols=cols,
        cell_width=50,
        cell_height=50,
        window=win,
    )
    maze.break_entrance_and_exit(0, 0)
    maze.break_entrance_and_exit(cols - 1, rows - 1)
    maze.break_walls(0, 0)
    for r in range(rows):
        for c in range(cols):
            maze.draw_cell(c, r)

    maze.reset_visited_cells()
    maze.solve_r(0, 0)

    win.wait_for_close()


if __name__ == "__main__":
    main()
