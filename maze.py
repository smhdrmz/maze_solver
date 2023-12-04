from graphics import *
from time import sleep
import random


class Cell:
    def __init__(self, win=None):
        self.__x1 = None
        self.__x2 = None
        self.__y1 = None
        self.__y2 = None
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__win = win
        self.visited = False

    def draw(self, x1, x2, y1, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        top_left = Point(self.__x1, self.__y1)
        top_right = Point(self.__x2, self.__y1)
        bot_left = Point(self.__x1, self.__y2)
        bot_right = Point(self.__x2, self.__y2)
        
        
        left_wall = Line(top_left, bot_left)
        self.__win.draw_line(left_wall, "black" if self.has_left_wall else "white")
        
        right_wall = Line(top_right, bot_right)
        self.__win.draw_line(right_wall, "black" if self.has_right_wall else "white")

        bot_wall = Line(bot_left, bot_right)
        self.__win.draw_line(bot_wall, "black" if self.has_bottom_wall else "white")

        top_wall = Line(top_left, top_right)
        self.__win.draw_line(top_wall, "black" if self.has_top_wall else "white")
    
    def draw_move(self, to_cell, undo=False):
        center_x = (self.__x1 + self.__x2) / 2
        center_y = (self.__y1 + self.__y2) / 2
        center = Point(center_x, center_y)

        to_center_x = (to_cell.__x1 + to_cell.__x2) / 2
        to_center_y = (to_cell.__y1 + to_cell.__y2) / 2
        to_center = Point(to_center_x, to_center_y)

        path = Line(center, to_center)

        if undo:
            self.__win.draw_line(path, "gray")
        else:
            self.__win.draw_line(path, "red")
            

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self.cells = [[] for i in range(num_rows)]

        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self.cells[i].append(Cell(self._win))
        
        if seed:
            random.seed(seed)
    
    def _create_cells(self):
        
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cell(i, j)
                self._animate()
    
    def _draw_cell(self, i , j):

        x1 = self._x1 + j * self._cell_size_x
        y1 = self._y1 + i * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self.cells[i][j].draw(x1, x2, y1, y2)

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        sleep(0.03)
    
    def _break_entrance_and_exit(self):
        entrance = self.cells[0][0]
        entrance.has_top_wall = False
        self._draw_cell(0, 0)
        self._animate()

        exit = self.cells[self._num_rows - 1][self._num_cols - 1]
        exit.has_bottom_wall = False
        self._draw_cell(self._num_rows - 1, self._num_cols - 1)
        self._animate()
    
    def _break_walls_r(self, i ,j):
        current = self.cells[i][j]
        current.visited = True
        while True:
            to_visit = []
            neighbors = [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]
            for neighbor in neighbors:
                if 0 <= neighbor[0] < self._num_rows and 0 <= neighbor[1] < self._num_cols:
                    if not self.cells[neighbor[0]][neighbor[1]].visited:
                        to_visit.append(neighbor)
            
            if not to_visit:
                return
            
            chosen_cell_idx = to_visit[random.randrange(len(to_visit))]
            chosen_cell = self.cells[chosen_cell_idx[0]][chosen_cell_idx[1]]

            if chosen_cell_idx[0] == i:
                if chosen_cell_idx[1] > j:
                    current.has_right_wall = False
                    chosen_cell.has_left_wall = False
                else:
                    current.has_left_wall = False
                    chosen_cell.has_right_wall = False
            else:
                if chosen_cell_idx[0] > i:
                    current.has_bottom_wall = False
                    chosen_cell.has_top_wall = False
                else:
                    current.has_top_wall = False
                    chosen_cell.has_bottom_wall = False
            
            self._draw_cell(i, j)
            self._animate()
            self._break_walls_r(chosen_cell_idx[0], chosen_cell_idx[1])

    def _reset_cells_visited(self):

        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self.cells[i][j].visited = False

    def _is_connected(self, current_cell, direction):
        if direction == "top":
            return not current_cell.has_top_wall
        if direction == "bottom":
            return not current_cell.has_bottom_wall
        if direction == "left":
            return not current_cell.has_left_wall
        if direction == "right":
            return not current_cell.has_right_wall


    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self.cells[i][j]
        current_cell.visited = True

        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True
        
        neighbors = [[i - 1, j, "top"], [i + 1, j, "bottom"], [i, j - 1, "left"], [i, j + 1, "right"]]

        for neighbor in neighbors:
                if (
                    0 <= neighbor[0] < self._num_rows and
                    0 <= neighbor[1] < self._num_cols and
                    self._is_connected(current_cell, neighbor[2]) and
                    not self.cells[neighbor[0]][neighbor[1]].visited
                ):
                    current_cell.draw_move(self.cells[neighbor[0]][neighbor[1]])
                    result = self._solve_r(neighbor[0], neighbor[1])

                    if result:
                        return True
                    current_cell.draw_move(self.cells[neighbor[0]][neighbor[1]], undo=True)

        return False
