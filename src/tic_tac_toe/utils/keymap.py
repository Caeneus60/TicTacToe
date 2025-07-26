import curses

class Keymap:
    """
    Defines basic key bindings for navigation and confirmation.
    Modify these sets directly to change the bindings.
    """

    def __init__(self):
        # Keys to confirm an action (Enter, Space)
        self.confirm = {10, 13, ord(' ')}  # 10=Enter, 13=Carriage Return

        # Keys to move up (Arrow Up, W/w)
        self.move_up = {curses.KEY_UP, ord("w"), ord("W")}

        # Keys to move down (Arrow Down, S/s)
        self.move_down = {curses.KEY_DOWN, ord("s"), ord("S")}
        
        # Keys to move left (Arrow Left, A/a)
        self.move_left = {curses.KEY_LEFT, ord("a"), ord("A")}
        
        # Keys to move right (Arrow Right, D/d)
        self.move_right = {curses.KEY_RIGHT, ord("d"), ord("D")}

        # Keys to go back (Escape)
        self.back = {27, ord("r"), ord("R")}  # 27=ESC

        # Keys to quit (Q/q)
        self.quit = {ord("q"), ord("Q")}

    def is_confirm(self, key: int) -> bool:
        return key in self.confirm

    def is_move_up(self, key: int) -> bool:
        return key in self.move_up

    def is_move_down(self, key: int) -> bool:
        return key in self.move_down
    
    def is_move_left(self, key: int) -> bool:
        return key in self.move_left
    
    def is_move_right(self, key: int) -> bool:
        return key in self.move_right

    def is_back(self, key: int) -> bool:
        return key in self.back

    def is_quit(self, key: int) -> bool:
        return key in self.quit
