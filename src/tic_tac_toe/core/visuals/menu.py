import curses
from enum import Enum
import time

from tic_tac_toe.core.visuals.art import TITLE, GOODBYE
from tic_tac_toe.utils.keymap import Keymap

MENU_OPTIONS = ["Start","Customize figure", "Exit"]

class MenuOptions(Enum):
    START = 0
    CUSTOMIZE = 1
    EXIT = 2

    @classmethod
    def list(cls):
        return [option for option in MENU_OPTIONS]
    
    @classmethod
    def count(cls):
        return len(MENU_OPTIONS)

class Menu:
    """
    Handles the main menu display and navigation using curses.
    """    
    
    def __init__(self):
        self.option_index = 0
        self.keymap = Keymap()
    
    @staticmethod
    def tune_middle_position(text: str, middle_x: int):
        """
        Calculates horizontal position to center text.
        """
        return max(0, middle_x - len(text) // 2)
    
    @staticmethod
    def initialize_colors():
        """
        Define color pairs for the menu interface.
        """
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)  # Highlight
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Title
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Message
    
    def draw_art(self, stdscr: curses.window, ART: str):
        """
        Draw ASCII art at a centered position.
        """
        _, w = stdscr.getmaxyx()
        y, _ = stdscr.getyx()
        
        art_lines = ART.strip("\n").split("\n")
        for line in art_lines:
            y += 1
            x = self.tune_middle_position(line, w // 2)
            stdscr.addstr(y, x, line, curses.A_BOLD | curses.color_pair(2))
    
    def draw_options(self, stdscr: curses.window, current_index: int):
        """
        Draw all menu options, highlighting current selection.
        """
        _, w = stdscr.getmaxyx()
        y, _ = stdscr.getyx()

        
        for i, option in enumerate(MENU_OPTIONS):
            if i == 0 :
                y += 1 # Give an extra space separate from the title.
                
            x = self.tune_middle_position(option, w // 2)
            
            if i == current_index:
                stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.A_BOLD | curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option, curses.color_pair(3))
                
            y += 1
            
    def draw_current_figure(self, stdscr: curses.window, player):
        """
        Displays current user figure on Menu.
        """
        stdscr.addstr("\nCurrent player figure:")
        stdscr.addstr(player.figure, curses.A_BOLD)
        stdscr.refresh()
            
    def navigate(self, stdscr: curses.window) -> MenuOptions:
        """
        Display the menu and allow navigation.
        Returns the selected MenuOptions value.
        """
        
        # Hide cursor
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        self.initialize_colors()
        
        while True:
            stdscr.clear()
            self.draw_art(stdscr, TITLE)
            self.draw_options(stdscr, self.option_index)
            stdscr.refresh()
            
            key = stdscr.getch()
            # Use % operand to make sure you're always within valid values.
            if self.keymap.is_move_up(key):
                self.option_index = (self.option_index - 1) % len(MENU_OPTIONS)
            elif self.keymap.is_move_down(key):
                self.option_index = (self.option_index + 1) % len(MENU_OPTIONS)
            elif self.keymap.is_quit(key):
                return MenuOptions.EXIT
            elif self.keymap.is_confirm(key):
                return MenuOptions(self.option_index)
        
        
    def close(self, stdscr: curses.window):
        """
        Display a goodbye message before exiting.
        """
        
        h, _ = stdscr.getmaxyx()
        
        stdscr.clear()        
        self.draw_art(stdscr, GOODBYE)
        
        stdscr.refresh()
        time.sleep(1.5)
