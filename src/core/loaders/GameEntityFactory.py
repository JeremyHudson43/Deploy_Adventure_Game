import logging
import adventurelib as adv
from pathlib import Path
from ..entities.NPC import NPC
from .GameDataParser import GameDataParser

logger = logging.getLogger(__name__)

class GameEntityFactory:
    """Handles creation and setup of individual game components."""
    
    def __init__(self, world):
        self.world = world
        self.json_loader = GameDataParser()

    def create_item(self, file_path: Path, level: str = None) -> None:
        """Create an item from JSON data."""
        try:
            item_data = self.json_loader.load_json_file(file_path)
            name = item_data['name']
            
            item = adv.Item(name)
            item.description = item_data.get('description', '')
            
            # Add additional properties
            for key, value in item_data.get('properties', {}).items():
                setattr(item, key, value)
            
            item_key = self.json_loader.construct_key(name, level)
            self.world.items[item_key] = item
            self.world.item_names[item_key] = name
            
        except Exception as e:
            logger.error(f"Error creating item from {file_path}: {str(e)}")
            raise

    def create_npc(self, file_path: Path, level: str = None) -> None:
        """Create an NPC from JSON data."""
        try:
            npc_data = self.json_loader.load_json_file(file_path)
            name = npc_data['name']
            npc_id = npc_data.get('id', name)  # Use id if available, fallback to name
            description = npc_data.get('description', '')
            dialogue = npc_data.get('dialogue', {})
            
            # Get greeting/default dialogue
            default_dialogue = dialogue.get('greeting') or dialogue.get('default') or "Hello!"
            npc = NPC(name, default_dialogue)
            npc.description = description
            
            # Store the entire dialogue structure for puzzle use
            npc.dialogue_data = dialogue
            
            # Add items
            for item_name in npc_data.get('items', []):
                item_key = self.json_loader.construct_key(item_name, level)
                if item_key in self.world.items:
                    npc.inventory.add(self.world.items[item_key])
            
            # Use id for the key instead of name
            npc_key = self.json_loader.construct_key(npc_id, level)
            self.world.npcs[npc_key] = npc
            
        except Exception as e:
            logger.error(f"Error creating NPC from {file_path}: {str(e)}")
            raise

    def create_room(self, file_path: Path, level: str = None) -> None:
        """Create a room from JSON data."""
        try:
            room_data = self.json_loader.load_json_file(file_path)
            room = adv.Room(room_data['description'])
            room.name = room_data['name']
            room.items = adv.Bag()
            room.npcs = []
            
            # Store both the file stem and normalized name for lookup
            file_id = f"{level}/{file_path.stem}" if level else file_path.stem
            normalized_name = self.json_loader.normalize_name(room.name)
            room_id = f"{level}/{normalized_name}" if level else normalized_name
            
            # Store room under both IDs for compatibility
            self.world.rooms[file_id] = room
            if file_id != room_id:
                self.world.rooms[room_id] = room
            
        except Exception as e:
            logger.error(f"Error creating room from {file_path}: {str(e)}")
            raise 