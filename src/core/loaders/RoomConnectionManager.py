import logging
from pathlib import Path
from .GameDataParser import GameDataParser
from adventurelib import Room

logger = logging.getLogger('world')

class RoomConnectionManager:
    """Handles connecting and populating world components."""
    
    def __init__(self, world):
        self.world = world
        self.json_loader = GameDataParser()

    def setup_room_connections(self, base_path: Path) -> None:
        """Set up room exits and connections."""
        
        # First pass: Set up basic exits
        for room_id, room in list(self.world.rooms.items()):  # Use list to allow dict modification
            try:
                room_data = self._get_room_data(room_id, base_path)
                self._setup_exits(room, room_data, room_id)
                self._populate_room(room, room_data, room_id)
            except FileNotFoundError as e:
                logger.warning(f"Room file not found for {room_id}, removing room: {str(e)}")
                del self.world.rooms[room_id]
            except Exception as e:
                logger.error(f"Error setting up room {room_id}: {str(e)}")
                raise
        
        # Second pass: Clean up invalid exits
        for room_id, room in list(self.world.rooms.items()):
            for exit_dir in room.exits():
                target_room = getattr(room, exit_dir)
                if target_room and target_room not in self.world.rooms.values():
                    logger.warning(f"Removing invalid exit {exit_dir} from room {room_id}")
                    setattr(room, exit_dir, None)

    def _get_room_data(self, room_id: str, base_path: Path) -> dict:
        """Get room data from file."""
        try:
            if '/' in room_id:
                level, room_name = room_id.split('/')
                # Try the original filename first
                path = base_path / level / 'rooms' / f"{room_name}.json"
                if path.exists():
                    return self.json_loader.load_json_file(path)
                
                # If that fails, try with normalized name
                normalized_path = base_path / level / 'rooms' / f"{self.json_loader.normalize_name(room_name)}.json"
                if normalized_path.exists():
                    return self.json_loader.load_json_file(normalized_path)
                    
                raise FileNotFoundError(f"Could not find room file for {room_id}")
            else:
                path = base_path / 'rooms' / f"{room_id}.json"
                return self.json_loader.load_json_file(path)
        except Exception as e:
            logger.error(f"Error loading room data for {room_id}: {str(e)}")
            raise

    def _setup_exits(self, room, room_data: dict, room_id: str) -> None:
        """Set up room exits."""
        # Get the current level from the room_id
        current_level = room_id.split('/')[0] if '/' in room_id else 'level_one'
        self.world.current_level = current_level
        
        # Create a single normalized room mapping
        normalized_rooms = {}
        for actual_id in self.world.rooms.keys():
            normalized_id = self.world._normalize_room_id(actual_id)
            normalized_rooms[normalized_id] = actual_id
        
        # Handle normal exits
        for direction, target_room_id in room_data.get('exits', {}).items():
            if direction == 'portal':  # Skip portal exits
                continue
            
            # Normalize target room ID
            if not target_room_id:
                continue
            
            # Use the world's normalization with current level context
            self.world.current_level = current_level
            normalized_target = self.world._normalize_room_id(target_room_id)
            
            if normalized_target in normalized_rooms:
                actual_key = normalized_rooms[normalized_target]
                setattr(room, direction, self.world.rooms[actual_key])
            else:
                logger.warning(f"Could not find room '{normalized_target}' for exit '{direction}' in room '{room_id}'")
        
        # Handle stairs as properties instead of exits
        if 'stairs_up' in room_data:
            room.stairs_up = room_data['stairs_up']
        if 'stairs_down' in room_data:
            room.stairs_down = room_data['stairs_down']

    def _populate_room(self, room, room_data: dict, room_id: str) -> None:
        """Populate room with items and NPCs."""
        level = room_id.split('/')[0] if '/' in room_id else None
        
        # Add items
        for item_name in room_data.get('items', []):
            item_key = self.json_loader.construct_key(item_name, level)
            if item_key in self.world.items:
                room.items.add(self.world.items[item_key])
            else:
                logger.warning(f"Item '{item_name}' not found for room '{room.name}'")
        
        # Add NPCs
        for npc_name in room_data.get('npcs', []):
            npc_key = self.json_loader.construct_key(npc_name, level)
            if npc_key in self.world.npcs:
                room.npcs.append(self.world.npcs[npc_key])
            elif npc_name in self.world.npcs:  # fallback
                room.npcs.append(self.world.npcs[npc_name])
            else:
                logger.warning(f"NPC '{npc_name}' not found for room '{room.name}'")

    def _normalize_room_id(self, target_room_id: str, current_room_id: str) -> str:
        """Normalize room ID while preserving path structure."""
        if '/' in target_room_id:
            return target_room_id.lower().replace(' ', '_').replace("'", '')
        else:
            level = current_room_id.split('/')[0] if '/' in current_room_id else 'level_one'
            normalized = target_room_id.lower().replace(' ', '_').replace("'", '')
            return f"{level}/{normalized}"

