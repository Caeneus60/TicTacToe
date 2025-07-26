import curses
import time
import curses.panel as panel

from enum import Enum, auto
from typing import Optional

from tic_tac_toe.core.ai.agents import RandomAI, TicTacToeAI
from tic_tac_toe.core.visuals.menu import Menu, MenuOptions
from tic_tac_toe.core.game.player import Player
from tic_tac_toe.core.game.board import Board
from tic_tac_toe.core.visuals.art import GAME_OVER, YOU_WIN, DRAW

from tic_tac_toe.utils.keymap import Keymap
        
class GameState(Enum):
    IN_MENU = auto()
    IN_GAME = auto()
    GAME_OVER = auto()
    
class GameMode(Enum):
    PVP = auto()
    CPU_EASY = auto()
    CPU_HARD = auto()
        
class GameLoop:
    """
    Main game controller that manages the menu, game state and transtitions.
    """
    
    MODE_OPTIONS = ["Player vs Player", "Player vs CPU (Easy)", "Player vs CPU (Hard)"]
    
    def __init__(self) -> None:
        self.menu = Menu()
        self.board = Board()
        self.current_game_state: Optional[GameState] = None
        self.keymap = Keymap()
        
        self.player_1 = Player(
                name = "Player 1",
                figure = "X",
                goes_first = True,
                is_cpu = False
                )
        
        self.player_2: Optional[Player] = None
        self.ai_agent = None

    # -----------------
    # run / main
    # -----------------
    
    def run(self) -> None:
        """
        Start the main gameloop.
        """
        curses.wrapper(self.main)
        
    def main(self, stdscr: curses.window) -> None:
        """Handle menu navigation and transitions"""
        while True:
            try:
                self._prep_screen(stdscr)
                stdscr.clear()
                self.current_game_state = GameState.IN_MENU
                
                stdscr.refresh()
                
                selected_option = self.menu.navigate(stdscr)
                
                if selected_option == MenuOptions.START:
                    self.current_game_state = GameState.IN_GAME
                    mode = self.select_mode(stdscr)
                    curses.wrapper(self.run_game, mode) if mode is not None else ValueError("GameMode shouldn't be None")
                elif selected_option == MenuOptions.CUSTOMIZE:
                    self.handle_customization(stdscr, self.player_1)
                elif selected_option == MenuOptions.EXIT:
                    self.exit_game(stdscr)
                    break
            
            except Exception as e:
                stdscr.clear()
                stdscr.addstr(5, 10, f"Error: {str(e)}")
                stdscr.refresh()
                stdscr.getch()
                break
            
    # -----------------
    # Mode selection
    # -----------------
    
    def select_mode(self, stdscr: curses.window) -> Optional[GameMode]:
        """
        Small in-loop menu to choose game mode.
        """
        index = 0
        self._prep_screen(stdscr)
        while self.current_game_state == GameState.IN_GAME:
            stdscr.clear()
            stdscr.addstr(1, 2, "Select Game Mode:", curses.A_BOLD)
            h, w = stdscr.getmaxyx()
            for i, opt in enumerate(self.MODE_OPTIONS):
                y = 3 + i
                x = 4
                if i == index:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, x, opt)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, opt)
            stdscr.refresh()
            
            key = stdscr.getch()
            if self.keymap.is_move_up(key):
                index = (index - 1) % len(self.MODE_OPTIONS)
            elif self.keymap.is_move_down(key):
                index = (index + 1) % len(self.MODE_OPTIONS)
            elif self.keymap.is_back(key):
                self.current_game_state = GameState.IN_MENU
                break
            elif self.keymap.is_confirm(key):
                if index == 0:
                    return GameMode.PVP
                elif index == 1:
                    return GameMode.CPU_EASY
                else:
                    return GameMode.CPU_HARD
        
    def run_game(self, stdscr: curses.window, mode: GameMode) -> None:
        """Run the actual Tic-Tac-Toe game"""
        
        try:
            self.board.reset()
            self._prep_screen(stdscr)
            
            # Set-up opponents
            
            if mode == GameMode.PVP:
                self.player_2 = Player(
                    name = "Player 2",
                    figure = "O",
                    goes_first = False,
                    is_cpu = False
                )
            else:
                cpu_name = "Randy" if mode == GameMode.CPU_EASY else "TicTaco"
                self.player_2 = Player(
                    name = cpu_name,
                    figure = "🦦" if cpu_name == "Randy" else "🌮",
                    goes_first = False,
                    is_cpu = True
                )
                self.ai_agent = RandomAI() if mode == GameMode.CPU_EASY else TicTacToeAI()
                
            current = self.player_1
            opponent = self.player_2
            
            while self.current_game_state == GameState.IN_GAME:
                stdscr.clear()
                self.board.draw(stdscr)
                stdscr.addstr(10, 2, f"Turn: {current.name} ({current.figure})")
                stdscr.addstr(12, 2, "Choose a position [1-9]: (q to quit, r to return to menu)")
                stdscr.refresh()
                
                if current.is_cpu:
                    move = self._cpu_move(current, opponent)
                else:
                    move = 0
                    while move == 0:
                        self.board.draw(stdscr)
                        stdscr.refresh()
                        
                        key = stdscr.getch()
                        move = self._read_move_from_keyboard(key)
                        if move == -1:
                            self.show_game_over(stdscr, "You quit the game.")
                            self.exit_game(stdscr)
                            break
                        if move == -2:
                            self.current_game_state = GameState.IN_MENU
                            break
                        
                        if move == 0:
                            move = self._handle_cursor_input(key)
                
                if not self.board.make_move(move, current.figure):
                    stdscr.addstr(14, 2, "Invalid move! Press any key to continue...")
                    stdscr.refresh()
                    stdscr.getch()
                    continue
                
                current.make_move(move)
                
                winner = self.board.check_winner()
                if winner == self.player_1.figure:
                    self.end_game(stdscr, YOU_WIN)
                    break
                elif winner == self.player_2.figure:
                    self.end_game(stdscr, GAME_OVER)
                    break
                
                if self.board.is_full():
                    self.end_game(stdscr, DRAW)
                    break

                # Switch player
                current, opponent = opponent, current
        finally:
            self.current_game_state = GameState.IN_MENU
            stdscr.clear()
            curses.flushinp()

    # -----------------
    # Helpers
    # -----------------
    
    def _read_move_from_keyboard(self, key: int) -> int:
        """
        Returns:
            1-9 -> Valid number move.
            -1 -> User pressed 'q' (quit)
            -2 -> User pressed 'r' or 'esc' (go to menu)
        """
        curses.curs_set(0)
        
        if self.keymap.is_quit(key):
            return -1
        elif self.keymap.is_back(key):
            return -2
        
        try:
            move = int(chr(key))
            return move
        
        except Exception:
            return 0 # Ignore other inputs.
        
    def _handle_cursor_input(self, key: int) -> int:
        """
        Allows navigation navigation of the board with the arrow keys/WASD.
        Returns the board position (1-9) or 0 if no move was confirmed.
        """        
        if self.keymap.is_move_up(key):
            self.board.move_cursor("up")
        elif self.keymap.is_move_down(key):
            self.board.move_cursor("down")
        elif self.keymap.is_move_left(key):
            self.board.move_cursor("left")
        elif self.keymap.is_move_right(key):
            self.board.move_cursor("right")
        elif self.keymap.is_confirm(key):
            row, col = self.board.get_cursor_position()
            pos = 1 + row * self.board.size + col
            if self.board.is_valid_move(pos):
                return pos

        return 0
        
    def _cpu_move(self, current: Player, opponent: Player) -> int:
        """
        Decides which move the CPU Player makes.
        Returns the 1-9 valid move made by either "Randy" or "TicTaco" :)
        """
        if isinstance(self.ai_agent, RandomAI):
            return self.ai_agent.choose_move(self.board, current.figure)
        elif isinstance(self.ai_agent, TicTacToeAI):
            return self.ai_agent.choose_move(self.board, current.figure, opponent.figure)
        raise RuntimeError("AI agent not initialized.")
    
    @staticmethod
    def _prep_screen(stdscr: curses.window):
        """
        Makes sure the game keeps working fine when restarting the game.
        Resets curses relevant display variables.
        """
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
    
    def handle_customization(self, stdscr: curses.window, player: Player) -> None:
        """
        Placeholder for future customization options.
        """
        
        index = 0
        COLS = 5           # how many figures per row
        START_Y = 3
        START_X = 4
        ROW_SPACING = 2    # vertical spacing between rows

        # compute a nice horizontal spacing based on the widest figure
        cell_w = max(len(f) for f in Player.figures) + 2  # +2 for padding

        while True:
            stdscr.clear()
            stdscr.addstr(1, 2, f"Current Player: {player.name}", curses.A_BOLD)
            stdscr.addstr(2, 3, "Select a custom figure:", curses.A_BOLD)

            for i, figure in enumerate(Player.figures):
                row = i // COLS
                col = i % COLS

                y = START_Y + row * ROW_SPACING
                x = START_X + col * cell_w

                if i == index:
                    stdscr.addstr(y + 1, x, figure)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, figure)

            stdscr.refresh()

            key = stdscr.getch()
            if self.keymap.is_move_left(key):
                index = (index - 1) % len(Player.figures)
            elif self.keymap.is_move_right(key):
                index = (index + 1) % len(Player.figures)
            elif self.keymap.is_move_up(key):
                # jump one row up (COLS positions back)
                index = (index - COLS) % len(Player.figures)
            elif self.keymap.is_move_down(key):
                # jump one row down (COLS positions forward)
                index = (index + COLS) % len(Player.figures)
            elif self.keymap.is_confirm(key):
                player.figure = Player.figures[index]
                break
            
    def end_game(self, stdscr, message: str) -> None:
        """
        Does all steps required to end the game properly.
        """
        self.current_game_state = GameState.GAME_OVER
        self.board.draw(stdscr)
        self.show_game_over(stdscr, message)
    
    def exit_game(self, stdscr:curses.window) -> None:
        """
        Show GOODBYE screen and exit.
        """
        self.menu.close(stdscr)
    
    def show_game_over(self, stdscr: curses.window, message: str) -> None:
        """
        Show the game over screen.
        """
        stdscr.clear()
        stdscr.addstr(message, curses.color_pair(2))
        stdscr.addstr("\nPress any key to return to the menu...", curses.color_pair(3))
        stdscr.refresh()
        curses.flushinp()
        stdscr.getch()
        time.sleep(0.25)
        self.current_game_state = GameState.IN_MENU
        
