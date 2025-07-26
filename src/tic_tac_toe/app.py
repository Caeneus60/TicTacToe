#!/bin/python3

"""
Entry point for the Tic-Tac-Toe game.
Initializes and runs the gameloop.
"""

from tic_tac_toe.gameloop import GameLoop

def main():
    game = GameLoop()
    game.run()

if __name__ == "__main__":
    main()
