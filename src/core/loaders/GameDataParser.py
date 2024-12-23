import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class GameDataParser:
    """Handles JSON file operations and basic path management."""
    
    @staticmethod
    def normalize_name(name: str) -> str:
        """Convert a name to its normalized form for comparison."""
        return name.lower().replace(' ', '_').replace("'", '').replace(chr(39), '')

    @staticmethod
    def load_json_file(file_path: Path) -> dict:
        """Load and parse a JSON file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {str(e)}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Required file not found: {file_path}")

    @staticmethod
    def get_level_dirs(world_path: Path) -> list:
        """Get all level directories in a world."""
        return [d for d in world_path.iterdir() 
                if d.is_dir() and d.name.startswith('level_')]

    @staticmethod
    def construct_key(name: str, level: str = None) -> str:
        """Construct a component key with optional level prefix."""
        normalized = GameDataParser.normalize_name(name)
        return f"{level}/{normalized}" if level else normalized 