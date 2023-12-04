import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_rows,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_cols,
        )
    
    def test_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_walls_r(0, 0)
        m1._reset_cells_visited()

        for i in range(num_rows):
            for j in range(num_cols):
                self.assertFalse(m1.cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()