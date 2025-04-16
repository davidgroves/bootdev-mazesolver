from tkinter import Tk, BOTH, Canvas
import sys

class Window:
    def __init__(self, width: int = 1280, height: int = 720, title: str = "Maze Solver"):
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

    def close(self):
        self.running = False

def main():
    win = Window(800, 600)
    win.wait_for_close()

if __name__ == "__main__":
    main()
