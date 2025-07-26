import unittest

from tic_tac_toe.core.game.board import Board

class TestBoard(unittest.TestCase):
    
    def setUp(self):
        self.board = Board()
        
    def test_initial_board_empty(self):
        self.assertEqual(self.board.get_available_moves(), list(range(1, 10)))
        self.assertIsNone(self.board.check_winner())
        self.assertFalse(self.board.is_full())
        
    def test_make_valid_move(self):
        self.assertTrue(self.board.make_move(1, "X"))
        self.assertFalse(self.board.is_valid_move(1))
        self.assertNotIn(1, self.board.get_available_moves())
        
    def test_reject_invalid_move_numbers(self):
        self.assertFalse(self.board.make_move(0, "X"))
        self.assertFalse(self.board.make_move(10, "X"))
        
    def test_reject_occupied_cell(self):
        self.assertTrue(self.board.make_move(1, "X"))
        self.assertFalse(self.board.make_move(1, "O"))
        
    def test_row_win(self):
        self.board.make_move(1, "X")
        self.board.make_move(2, "X")
        self.board.make_move(3, "X")
        self.assertEqual(self.board.check_winner(), "X")

    def test_col_win(self):
        self.board.make_move(1, "O")
        self.board.make_move(4, "O")
        self.board.make_move(7, "O")
        self.assertEqual(self.board.check_winner(), "O")

    def test_diag_win(self):
        self.board.make_move(1, "X")
        self.board.make_move(5, "X")
        self.board.make_move(9, "X")
        self.assertEqual(self.board.check_winner(), "X")

    def test_antidiag_win(self):
        self.board.make_move(3, "O")
        self.board.make_move(5, "O")
        self.board.make_move(7, "O")
        self.assertEqual(self.board.check_winner(), "O")
        
    def test_draw(self):
        moves = [
            (1, "X"), (2, "O"), (3, "X"),
            (6, "O"), (5, "X"), (4, "X"),
            (7, "O"), (8, "X"), (9, "O"),
        ]
        for pos, fig in moves:
            self.assertTrue(self.board.make_move(pos, fig))
        self.assertIsNone(self.board.check_winner())
        self.assertTrue(self.board.is_full())
        
if __name__ == "__main__":
    unittest.main()