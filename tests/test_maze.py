import src.mazesolver.main as main


def test_maze_create_cells():
    cols = 12
    rows = 10
    maze = main.Maze(0, 0, rows, cols, cols, rows)
    assert len(maze.cells) == rows
    assert len(maze.cells[0]) == cols

def test_maze_break_entrance_and_exit():
    cols = 10
    rows = 10
    maze = main.Maze(0, 0, rows, cols, cols, rows)
    maze.break_entrance_and_exit(0, 0)
    maze.break_entrance_and_exit(cols - 1, rows - 1)

    assert maze.cells[0][0].walls == main.Sides.TOP | main.Sides.BOTTOM | main.Sides.RIGHT
    assert maze.cells[cols - 1][rows - 1].walls == main.Sides.TOP | main.Sides.BOTTOM | main.Sides.LEFT