from typing import List, Optional

class Player:
    """
    Represents a Tic-Tac-Toe player (human or CPU).
    """
    
    figures = [
        "X", "O", "🔥", "🫥", "🐺",
        "🧊", "🥀", "👌", "🤡", "🥸",
        "😡", "🎯", "💎", "🧸", "🎀"
    ]
    
    def __init__(self, name: str = "Player", figure: str = "X", goes_first: bool = True, is_cpu: bool = False) -> None:
        self.name = name
        self.goes_first = goes_first
        self.figure = figure
        self.is_cpu = is_cpu
        
        self.turn: Optional[int] = None
        self.moves: List[int] = []
        
    def reset(self) -> None:
        self.turn = None
        self.moves.clear()
        
    def make_move(self, choice) -> None:
        self.moves.append(choice)
        
    def get_moves_left(self) -> None:
        total_moves = 5 if self.goes_first else 4
        self.moves_left = total_moves - len(self.moves)
        
    def get_last_move(self) -> int:
        return self.moves[-1] if self.moves else -1