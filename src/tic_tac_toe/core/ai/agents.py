import math
import random

from typing import Optional, Tuple

from tic_tac_toe.core.game.board import Board

class RandomAI:
    """
    Chooses any available move at random.
    """
    
    def choose_move(self, board: Board, figure: str) -> int:
        return random.choice(board.get_available_moves())
    
class TicTacToeAI:
    """
    Tic-Tac-Toe AI using Minimax.
    """
    
    def choose_move(self, board: Board, figure: str, opponent: str) -> int:
        best_score = -math.inf
        best_move = None

        for move in board.get_available_moves():
            # simulate
            board.make_move(move, figure)
            score = self._minimax(board, False, figure, opponent)
            # undo
            board.current_state = self._undo_move(board, move)
            if score > best_score:
                best_score = score
                best_move = move

        # Fallback if something weird happens
        if best_move is None:
            return random.choice(board.get_available_moves())
        return best_move
    
    #--------------
    # Helpers
    #--------------

    def _minimax(self, board: Board, maximizing: bool, figure: str, opponent: str) -> float:
        """
        Minimax algorithm implementation.
        """
        winner = board.check_winner()
        if winner == figure:
            return 1
        elif winner == opponent:
            return -1
        elif board.is_full():
            return 0

        if maximizing:
            best_score = -math.inf
            for move in board.get_available_moves():
                board.make_move(move, figure)
                score = self._minimax(board, False, figure, opponent)
                board.current_state = self._undo_move(board, move)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for move in board.get_available_moves():
                board.make_move(move, opponent)
                score = self._minimax(board, True, figure, opponent)
                board.current_state = self._undo_move(board, move)
                best_score = min(best_score, score)
            return best_score

    def _undo_move(self, board: Board, move: int):
        """
        Returns a *new* board state after undoing `move`.
        This is a light workaround to avoid deep-copying the whole board repeatedly.
        """
        i, j = board.valid_moves[move]
        # Copy the board shallowly but recreate the row to avoid aliasing
        new_state = [row[:] for row in board.current_state]
        new_state[i][j] = " "
        return new_state
    