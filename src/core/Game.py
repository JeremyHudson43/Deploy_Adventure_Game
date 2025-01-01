"""
Path: src/core/game.py
"""

import json
import os
from pathlib import Path
from typing import Optional
import traceback
import adventurelib as adv

from core.world.GameWorld import GameWorld
from core.entities.Player import Player
from command_system.CommandProcessor import CommandProcessor
from core.systems.DisplayManager import DisplayManager as Display
from puzzles.core.BasePuzzle import BasePuzzle
from core.systems.GameState import GameState
from core.world.DirectionManager import initialize_directions

from core.systems.BossBattle import BossBattle

class Game:
    def __init__(self):
        # Existing initialization
        self.display = Display()
        self.game_state = GameState(self)
        self.player = Player()
        self.player.game = self
        self.worlds = {}
        self.current_world = None
        self.command_processor = CommandProcessor(self, self.player, self.display, self.game_state)
        self.is_running = True
        self.boss_battle = BossBattle(self)

    def serialize(self):
        return {
            'worlds': {name: world.name for name, world in self.worlds.items()},
            'current_world': self.current_world.name if self.current_world else None,
            'is_running': self.is_running
        }

    def deserialize(self, data):
        self.is_running = data.get('is_running', True)  # Default to True if not found
        self.load_all_worlds()
        current_world_name = data.get('current_world')
        if current_world_name and current_world_name in self.worlds:
            self.current_world = self.worlds[current_world_name]
            self.current_world.initialize(self.game_state)
            
    def setup(self):
        """Initialize game state and starting location."""
        # Load all worlds if not already loaded
        if not self.worlds:
            self.load_all_worlds()
        
        # Try to get Intro World
        self.current_world = self.worlds.get("Intro World")
        if not self.current_world:
            # If Intro World not found, try to use any available world
            if self.worlds:
                self.current_world = next(iter(self.worlds.values()))
            else:
                raise ValueError("No game worlds could be loaded. Please check your game files.")
                
        # Initialize the current world
        self.current_world.initialize(self.game_state)
            
        # Get starting room
        starting_room = self.current_world.get_starting_room()
        if not starting_room:
            raise ValueError(f"No starting room found in {self.current_world.name}. Please check world configuration.")
            
        self.player.move_to(starting_room)
        self.intro()
        self.command_processor.look()

    def load_all_worlds(self):
        """Load all game worlds from data files."""
        worlds_data = self._load_worlds_data()
        for world_id, world_info in worlds_data.items():
            try:
                # Create and load world
                new_world = GameWorld(world_id)
                new_world.load_world()
                
                # Store world using its configured name
                self.worlds[new_world.name] = new_world
                self.display.print_message(f"Successfully loaded world: {new_world.name}")
                
            except Exception as e:
                self.display.print_message(f"Error loading world '{world_id}':")
                self.display.print_message(traceback.format_exc())
                continue

        if not self.worlds:
            self.display.print_simple_message("Warning: No game worlds could be loaded. Please check your data files.")
            exit(1)

    def _load_worlds_data(self):
        """Load world configuration data from worlds.json."""
        # Go up 3 levels from src/core/ to project root
        base_path = Path(__file__).parent.parent.parent  # From src/core/ to project root
        data_path = base_path / 'data'
        worlds_file = data_path / 'worlds.json'
        
        if not worlds_file.exists():
            raise FileNotFoundError(f"worlds.json not found at {worlds_file}")
        
        with open(worlds_file, 'r') as f:
            return json.load(f)

    def intro(self):
        """Display game introduction message."""
        self.display.print_decorated(
            "Welcome to Tezzeret's Surreal Adventure\n\n"
            "Type 'help' at any time to see available actions."
        )
        
    def run(self):
        """Main game loop."""
        self.setup()
        while self.is_running:
            try:
                user_input = input("> ").strip()
                if not user_input:
                    continue
                self.command_processor.process_command(user_input)
                self.boss_battle.trigger_battle()
            except (EOFError, KeyboardInterrupt):
                self.quit()
            except Exception as e:
                self.display.print_message(f"An error occurred: {str(e)}")
                self.display.print_message(traceback.format_exc())  # Print full traceback for debugging

    def quit(self):
        """Clean up and exit the game."""
        self.is_running = False
        
    def get_puzzle(self, puzzle_id: str) -> Optional[BasePuzzle]:
        """Get a puzzle by its ID from the current world."""
        if self.current_world and hasattr(self.current_world, 'puzzles'):
            return self.current_world.puzzles.get(puzzle_id)
        return None

    def change_world(self, new_world):
        """Changes the current world and sets the player in the world's starting room."""
        self.current_world = new_world
        # Initialize the new world with game state
        new_world.initialize(self.game_state)
        self.player.state.current_world_id = new_world.name  # Track world in player state
        starting_room = new_world.get_starting_room()
        
        if starting_room:
            self.player.move_to(starting_room)
            self.command_processor.look()
        else:
            self.display.print_simple_message(f"Warning: No starting room found in {new_world.name}. Please check the world configuration.")
