"""
Path: src/core/player.py

Player class representing the game's player entity and state.
Acts as the central model for player-related data and operations.
"""

from adventurelib import Item, Bag
from typing import Optional, Set, Dict, Any
from dataclasses import dataclass, field

@dataclass
class PlayerState:
    """Represents saveable/loadable player state"""
    inventory: Bag = field(default_factory=Bag)
    visited_rooms: Set[str] = field(default_factory=set)
    current_room_id: Optional[str] = None
    current_world_id: Optional[str] = None
    discovered_commands: Set[str] = field(default_factory=set)
    attributes: Dict[str, Any] = field(default_factory=dict)

class Player:
    def __init__(self):
        self.current_room = None  # Runtime reference to actual room
        self.state = PlayerState()
        self.game = None  # Will be set by Game class
    
    def move_to(self, room) -> None:
        """Move player to a new room and record the visit"""
        self.current_room = room
        if hasattr(room, 'name'):
            self.state.visited_rooms.add(room.name)
            self.state.current_room_id = room.name
            
            # Update current_room for active puzzles
            if self.game and hasattr(self.game, 'current_world'):
                for puzzle in self.game.current_world.puzzles.values():
                    if puzzle.is_puzzle_room(room.name):
                        puzzle.current_room = room.name

    def has_visited(self, room_name: str) -> bool:
        """Check if player has previously visited a room"""
        return room_name in self.state.visited_rooms

    @property
    def inventory(self) -> Bag:
        """Access to player's inventory"""
        return self.state.inventory

    def discover_command(self, command: str) -> None:
        """Record that player has discovered a new command"""
        self.state.discovered_commands.add(command)

    def knows_command(self, command: str) -> bool:
        """Check if player has discovered a command"""
        return command in self.state.discovered_commands

    def get_attribute(self, key: str, default: Any = None) -> Any:
        """Get a custom player attribute"""
        return self.state.attributes.get(key, default)

    def set_attribute(self, key: str, value: Any) -> None:
        """Set a custom player attribute"""
        self.state.attributes[key] = value

    def serialize(self) -> dict:
        """Convert player state to serializable format"""
        return {
            'inventory': [item.name for item in self.state.inventory],
            'visited_rooms': list(self.state.visited_rooms),
            'current_room_id': self.state.current_room_id,
            'current_world_id': self.state.current_world_id,
            'discovered_commands': list(self.state.discovered_commands),
            'attributes': self.state.attributes
        }

    def deserialize(self, data):
        """Restore player state from serialized data."""
        try:
            # Create new state with provided data
            self.state = PlayerState(
                inventory=Bag([Item(name) for name in data.get('inventory', [])]),
                visited_rooms=set(data.get('visited_rooms', [])),
                current_room_id=data.get('current_room_id'),
                current_world_id=data.get('current_world_id'),
                discovered_commands=set(data.get('discovered_commands', [])),
                attributes=data.get('attributes', {})
            )
            return True
        except Exception as e:
            logger.error(f"Error deserializing player state: {str(e)}")
            return False