import curses

from typing import List, Dict, Tuple, Optional

from tic_tac_toe.core.game.player import Player

from wcwidth import wcswidth

class Board:
    """
    Tic-Tac-Toe board model & renderer.
    Keeps state, validates/applies moves, and detects winners.
    """

    def __init__(self, size: int = 3) -> None:
        if size != 3:
            raise ValueError("This implementation currently supports only 3x3 boards.")
        
        self.size = size
        self.playable: bool = True
        self.current_state: List[List[str]] = self._empty_board()
        self.valid_moves: Dict[int, Tuple[int, int]] = self._build_valid_moves()
        
        self.cursor_row = 0
        self.cursor_col = 0
        
    def move_cursor(self, direction: str) -> None:
        """
        Moves the cursor within the grid.
        """
        if direction == "up":
            self.cursor_row = (self.cursor_row - 1) % self.size
        elif direction == "down":
            self.cursor_row = (self.cursor_row + 1) % self.size
        elif direction == "left":
            self.cursor_col = (self.cursor_col - 1) % self.size
        elif direction == "right":
            self.cursor_col = (self.cursor_col + 1) % self.size
            
    def get_cursor_position(self) -> Tuple[int, int]:
        """
        Return the (row, col) of the current cursor.
        """
        return self.cursor_row, self.cursor_col
    
    def apply_cursor_move(self, figure: str) -> bool:
        """
        Place a figure at the cursor position.
        Returns True the move is valid, False otherwise.
        """
        row, col = self.cursor_row, self.cursor_col
        if self.current_state[row][col] == " ":
            self.current_state[row][col] = figure
            return True
        return False
            
    def reset(self) -> None:
        """
        Clear the board to its initial state.
        """
        self.current_state = self._empty_board()
        self.playable = True

    @staticmethod
    def _pad_to_width(s: str, width: int) -> str:
        """
        Pad `s` to fill exactly `width` terminal columns.
        """
        pad_len = width - wcswidth(s)
        return s + (" " * max(0, pad_len))
    
    
    def draw(self, stdscr, top: int = 2, left: int = 2) -> None:
        """
        Draw the board on the screen using curses.
        `top` and `left` offset the drawing position.
        """
        max_fig_width = max(
            (wcswidth(cell) for row in self.current_state for cell in row if cell),
            default=1
        )
        cell_width = max(3, max_fig_width + 2)  # at least 3 columns

        horizontal = ("─" * cell_width + "┼") * (self.size - 1) + ("─" * cell_width)

        for i in range(self.size):
            x_offset = 0
            for j in range(self.size):
                y = top + i * 2
                x = left + j * (cell_width + 1)  # +1 for the vertical line

                figure = self.current_state[i][j] if self.current_state[i][j] else " "
                cell_str = self._pad_to_width(f" {figure} ", cell_width)

                if (i, j) == (self.cursor_row, self.cursor_col):
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, cell_str)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, cell_str)

                if j < self.size - 1:
                    stdscr.addstr(y, x + cell_width, "│")

            # Draw horizontal line between rows
            if i < self.size - 1:
                stdscr.addstr(top + i * 2 + 1, left, horizontal)
                
    def clone(self) -> "Board":
        """
        Board cloning implementation for the Minmax AI.
        """
        new_board = Board(size = self.size)
        new_board.current_state = [row[:] for row in self.current_state]
        
        return new_board
                    
    def is_valid_move(self, pos: int) -> bool:
        """
        Determines whether a move is valid or not.
        Returns True if a move is valid, False otherwise.
        """
        move = self.valid_moves.get(pos)
        if not move:
            return False
        i, j = move
        return self.current_state[i][j] == " "
    
    def make_move(self, pos: int, figure: str) -> bool:
        """
        Attempt to make move with the given figure.
        Returns True on success, False if invalid.
        """
        if not self.is_valid_move(pos):
            return False
        
        i, j = self.valid_moves[pos]
        self.current_state[i][j] = figure
        
        return True
        
    
    def check_winner(self) -> Optional[str]:
        """
        Checks whether there's a winner in the board or not.
        Returns the symbol of the winner if there is one, None otherwise.
        """
        lines = self._winning_lines()
        
        for line in lines:
            symbols = [self.current_state[i][j] for i, j in line]
            if symbols[0] and all(cell == symbols[0] for cell in symbols):
                return symbols[0]
        return None 
    
    def is_full(self) -> bool:
        """
        Returns True if the board has no empty spaces left.
        """
        return all(cell != " " for row in self.current_state for cell in row)
    
    def get_available_moves(self) -> List[int]:
        """
        Returns a numeric list showing the current available moves on the board.
        """
        return [pos for pos, (i,j) in self.valid_moves.items() if self.current_state[i][j] == " "]
    
    # ----------
    # Helpers
    # ----------
    
    def _empty_board(self) -> List[List[str]]:
        return [[" " for _ in range(self.size)] for _ in range(self.size)]
    
    def _build_valid_moves(self) -> Dict[int, Tuple[int, int]]:
        """
        Build the board.
        Has compatibility if you want to expand the board size.
        """
        mapping: Dict[int, Tuple[int, int]] = {}
        num = 1
        for i in range(self.size):
            for j in range(self.size):
                mapping[num] = (i, j)
                num += 1
        return mapping
    
    def _winning_lines(self) -> List[List[Tuple[int, int]]]:
        """
        Return all index triplets that constitute winning lanes:
        rows, columns, diagonals.
        """
        lines: List[List[Tuple[int, int]]] = []
        
        # Rows
        for i in range(self.size):
            lines.append([(i, j) for j in range(self.size)])
            
        # Columns
        for j in range(self.size):
            lines.append([(i, j) for i in range(self.size)])
            
        # Diagonals
        lines.append([(i, i) for i in range(self.size)])
        lines.append([(i, self.size - 1 - i) for i in range(self.size)])
        
        return lines