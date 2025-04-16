import pytest
import src.mazesolver.main as main

def test_maze_create_cells():
    cols = 12
    rows = 10
    maze = main.Maze(0, 0, rows, cols, cols, rows)
    assert len(maze.cells) == rows
    assert len(maze.cells[0]) == cols
