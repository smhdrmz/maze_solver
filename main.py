from graphics import *
from maze import *

def main():
    win = Window(800, 600)
    

    maze = Maze(10, 10, 20, 20, 30, 30, win)
    maze._create_cells()
    maze._break_entrance_and_exit()
    maze._break_walls_r(0, 0)
    maze._reset_cells_visited()
    maze.solve()
    win.wait_for_close()

    
main()