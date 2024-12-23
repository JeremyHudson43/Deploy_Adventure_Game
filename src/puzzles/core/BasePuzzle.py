from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any, Set, Callable
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # Only show warnings and errors

@dataclass
class BasePuzzle(ABC):
    """
    Base class for all puzzles.
    """
    puzzle_type: str
    puzzle_id: str
    name: str
    description: str
    steps: List[Dict] = field(default_factory=list)
    rooms: Dict[str, str] = field(default_factory=dict)
    dialogue: Dict[str, str] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    completed: bool = False
    current_room: str = None
    game: Any = None  # Reference to game state

    def __post_init__(self):
        """Validate required fields after initialization"""
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate puzzle configuration"""
        required_fields = ['puzzle_id', 'name', 'description']
        missing = [f for f in required_fields if not getattr(self, f, None)]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

    def _normalize_name(self, name: str) -> str:
        """Normalize a name for comparison."""
        if name:
            return name.lower().replace("'", "").replace(" ", "_")
        return ""

    def _normalize_room_id(self, room_id: str) -> str:
        """Normalize room ID to match config format."""
        if not room_id:
            return ""
        room_id = self._normalize_name(room_id)
        if not room_id.startswith("level_"):
            room_id = f"level_one/{room_id}"
        return room_id

    def _get_normalized_inventory(self, inventory: List[Any]) -> Set[str]:
        """Convert inventory items to a set of normalized names."""
        normalized = set()
        for item in inventory:
            item_name = item.name if hasattr(item, 'name') else str(item)
            normalized.add(self._normalize_name(item_name))
        return normalized

    def get_command_handlers(self) -> Dict[str, Callable]:
        """Return a mapping of normalized command names to handler methods."""
        return {}

    def handle_command(self, command: str, *args, **kwargs) -> Tuple[bool, str]:
        """Handle a puzzle-specific command."""
        command_handlers = self.get_command_handlers()
        command_normalized = self._normalize_name(command)
        
        handler = command_handlers.get(command_normalized)
        if handler:
            return handler(command, *args, **kwargs)
        return False, "Unknown command."

    def get_room_description_addon(self, room_id: str) -> Optional[str]:
        """
        Get additional room description based on puzzle state.

        Args:
            room_id (str): Current room identifier

        Returns:
            Optional[str]: Additional description text or None
        """
        return None

    def check_completion(self) -> Tuple[bool, str]:
        """
        Check if puzzle is completed.

        Returns:
            Tuple[bool, str]: (is completed, status message)
        """
        return self.completed, "Puzzle complete!" if self.completed else "Puzzle not yet complete."

    def mark_completed(self) -> None:
        """Mark the puzzle as completed."""
        self.completed = True

    def get_available_commands(self, room_id: str) -> List[str]:
        """
        Get list of available commands in the current room.

        Args:
            room_id (str): Current room identifier

        Returns:
            List[str]: List of available commands
        """
        if self.is_puzzle_room(room_id):
            return list(self.commands.keys())
        else:
            return []

    def serialize(self) -> Dict[str, Any]:
        """
        Convert puzzle state to serializable format.

        Returns:
            Dict[str, Any]: Serialized puzzle state
        """
        return {
            'puzzle_id': self.puzzle_id,
            'name': self.name,
            'description': self.description,
            'type': self.puzzle_type,
            'completed': self.completed,
            'steps': self.steps,
            'rooms': self.rooms,
            'dialogue': self.dialogue,
            'config': self.config
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'BasePuzzle':
        """
        Create a puzzle instance from serialized data.

        Args:
            data (Dict[str, Any]): Serialized puzzle data

        Returns:
            BasePuzzle: New puzzle instance
        """
        return cls(**data)

    def handle_npc_dialogue(self, npc_name: str, topic: str, inventory: List[Any]) -> Optional[str]:
        """Handle NPC dialogue. Can be overridden by subclasses."""
        return None

    def get_hints(self, room_id: str) -> Optional[str]:
        """Get context-specific hints based on location and progress."""
        return None
