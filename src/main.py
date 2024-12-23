# main.py
from pathlib import Path

from core.Game import Game
from core.systems.LoggingConfig import setup_logging

def main():
    # Set up logging
    loggers = setup_logging()
    
    # Initialize and run game
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
