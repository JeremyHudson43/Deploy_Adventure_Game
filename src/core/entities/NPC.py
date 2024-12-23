# npc.py

from adventurelib import Bag
from typing import Dict, Any, Optional

class NPC:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.dialogue: Dict[str, Any] = {}
        self.inventory = Bag()
        self.state: Dict[str, Any] = {}  # For tracking NPC-specific states

    def add_dialogue(self, key: str, value: Any) -> None:
        """Add a dialogue entry to the NPC."""
        self.dialogue[key] = value

    def add_to_inventory(self, item: Any) -> None:
        """Add an item to the NPC's inventory."""
        self.inventory.add(item)

    def remove_from_inventory(self, item: Any) -> None:
        """Remove an item from the NPC's inventory."""
        self.inventory.take(item)

    def set_state(self, key: str, value: Any) -> None:
        """Set a state value for the NPC."""
        self.state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a state value for the NPC."""
        return self.state.get(key, default)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"NPC(name='{self.name}')"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NPC':
        """Create an NPC instance from a dictionary."""
        npc = cls(data['name'])
        npc.description = data.get('description', '')
        
        # Load dialogue
        dialogue = data.get('dialogue', {})
        for key, value in dialogue.items():
            npc.add_dialogue(key, value)
        
        # Load initial state if present
        initial_state = data.get('initial_state', {})
        for key, value in initial_state.items():
            npc.set_state(key, value)
        
        # Load inventory items if present
        inventory_items = data.get('inventory', [])
        for item in inventory_items:
            npc.add_to_inventory(item)
        
        return npc