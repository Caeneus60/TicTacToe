import unittest

from tic_tac_toe.core.game.board import Board
from tic_tac_toe.core.ai.agents import RandomAI, TicTacToeAI


class TestAI(unittest.TestCase):

    def test_random_ai_returns_legal_move(self):
        b = Board()
        b.make_move(1, "X")
        ai = RandomAI()
        move = ai.choose_move(b, "O")
        self.assertIn(move, b.get_available_moves())

    def test_minimax_ai_wins_if_possible(self):
        # X X _
        # _ O _
        # _ _ O
        b = Board()
        b.make_move(1, "X")
        b.make_move(2, "X")
        b.make_move(5, "O")
        b.make_move(9, "O")

        ai = TicTacToeAI()
        move = ai.choose_move(b, "X", "O")
        self.assertEqual(move, 3)  # Winning move

    def test_minimax_ai_blocks_if_needed(self):
        # O O _
        # _ X _
        # _ _ X
        b = Board()
        b.make_move(1, "O")
        b.make_move(2, "O")
        b.make_move(5, "X")
        b.make_move(9, "X")

        ai = TicTacToeAI()
        # 'O' is opponent, 'X' is figure in this test (or vice versa).
        # Use parameters consistently with your choose_move definition.
        move = ai.choose_move(b, "X", "O")  # figure='X', opponent='O'
        # X should block (3) to prevent O from winning.
        self.assertEqual(move, 3)


if __name__ == "__main__":
    unittest.main()
