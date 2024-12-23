import logging
from pathlib import Path
from typing import Dict, Type
from puzzles.core.BasePuzzle import BasePuzzle

logger = logging.getLogger(__name__)

class PuzzleManager:
    """Simplified manager that loads puzzles from types directory."""
    
    def __init__(self, world):
        self.world = world
        self.puzzles: Dict[str, BasePuzzle] = {}
        self._puzzle_types: Dict[str, Type[BasePuzzle]] = {}
        
        # Load puzzles from types directory
        self._load_puzzle_types()

    def _load_puzzle_types(self) -> None:
        """Load puzzles from the types directory."""
        try:
            # Get path to types directory
            types_dir = Path(__file__).parent.parent / 'types'
            
            if not types_dir.exists():
                logger.error(f"Puzzle types directory not found: {types_dir}")
                return

            # Look for Python files directly in types directory
            for puzzle_file in types_dir.glob('*.py'):
                if puzzle_file.stem == '__init__':
                    continue
                    
                # Import the puzzle module
                module_path = f"puzzles.types.{puzzle_file.stem}"
                try:
                    module = __import__(module_path, fromlist=['*'])
                    
                    # Look for puzzle classes in the module
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        
                        # Check if it's a puzzle class
                        if (isinstance(item, type) and 
                            issubclass(item, BasePuzzle) and 
                            item != BasePuzzle and
                            hasattr(item, 'puzzle_type')):
                            
                            # Register the puzzle type
                            self._puzzle_types[item.puzzle_type] = item
                            logger.info(f"Registered puzzle type: {item.puzzle_type}")
                            
                except Exception as e:
                    logger.error(f"Error loading puzzle {puzzle_file.name}: {str(e)}")

        except Exception as e:
            logger.error(f"Error loading puzzle types: {str(e)}")

    def initialize_world_puzzles(self) -> None:
        """Initialize puzzles for the current world."""
        try:
            # Create appropriate puzzles for this world
            if "Elemental Conflux" in self.world.name:
                air_puzzle_class = self._puzzle_types.get("air_mastery")
                if air_puzzle_class:
                    puzzle = air_puzzle_class()
                    self._add_puzzle(puzzle)
                    
            # Add other world-specific puzzles as needed
            
        except Exception as e:
            logger.error(f"Error initializing puzzles: {str(e)}")

    def _add_puzzle(self, puzzle: BasePuzzle) -> None:
        """Add a puzzle instance to the manager."""
        if hasattr(self.world, 'game'):
            puzzle.game = self.world.game
            
        self.puzzles[puzzle.puzzle_id] = puzzle
        self.world.puzzles[puzzle.puzzle_id] = puzzle

    def get_puzzle(self, puzzle_id: str) -> BasePuzzle:
        """Get a puzzle by its ID."""
        return self.puzzles.get(puzzle_id)