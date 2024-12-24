# src/core/world/game_world.py

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, List, Any, Set

# Core game components
from adventurelib import Room, Item, Bag

# Entity imports
from core.entities.NPC import NPC
from core.entities.Player import Player

# Puzzle system
from puzzles.core.BasePuzzle import BasePuzzle

# World component management
from core.world.WorldComponentLoader import WorldComponentLoader
from core.loaders.RoomConnectionManager import RoomConnectionManager
from puzzles.core.PuzzleManager import PuzzleManager

# Data handling
from core.loaders.GameDataParser import GameDataParser
from core.loaders.GameEntityFactory import GameEntityFactory

# Progression system
from core.systems.ProgressionSystem import ProgressionSystem


@dataclass
class GameWorldConfig:
    """Configuration data for a game world"""
    name: str
    description: str
    starting_room: str
    sequence_enabled: bool = False
    custom_settings: Dict = field(default_factory=dict)

class GameWorld:
    """
    Manages a complete game world, including loading, state management,
    and component coordination.
    """
    def __init__(self, world_id: str):
        self.world_id = world_id
        self.name: str = ""
        self.config: Optional[GameWorldConfig] = None
        
        # World components
        self.rooms: Dict[str, Room] = {}
        self.items: Dict[str, Item] = {}
        self.npcs: Dict[str, NPC] = {}
        self.puzzles: Dict[str, BasePuzzle] = {}
        self.item_names: Dict[str, str] = {}  # For looking up original names
        
        # Component managers
        self.component_loader = WorldComponentLoader(self)
        self.puzzle_manager = PuzzleManager(self)
        self.room_connector = RoomConnectionManager(self)
        self.data_parser = GameDataParser()
        self.entity_factory = GameEntityFactory(self)
        
        # Logging
        self.logger = logging.getLogger(f'world.{world_id}')

        # Game state and progression
        self.game_state = None
        self.progression = None
        self.current_level = "level_one"  # Default level

    # Then in GameWorld.py, modify initialize():
    def initialize(self, game_state):
        """Initialize the world with game state."""
        self.game_state = game_state
        self.game = game_state.game  # Make sure game reference is set
        self.progression = ProgressionSystem(game_state)
        self.load_world()

    def serialize(self):
        return {
            'name': self.name,
            'world_id': self.world_id,
            'rooms': {rid: self._serialize_room(room) for rid, room in self.rooms.items()},
            'items': {iid: self._serialize_item(item) for iid, item in self.items.items()},
            'npcs': {nid: self._serialize_npc(npc) for nid, npc in self.npcs.items()},
            'puzzles': {pid: puzzle.serialize() for pid, puzzle in self.puzzles.items()}
        }

    def _serialize_room(self, room):
        return {
            'name': room.name,
            'description': room.description,
            'items': [item.name for item in room.items],
            'npcs': [npc.name for npc in getattr(room, 'npcs', [])],
            'exits': {dir: getattr(room, dir).name if hasattr(getattr(room, dir), 'name') else getattr(room, dir) 
                     for dir in room.exits()},
            'stairs_up': room.stairs_up.name if hasattr(getattr(room, 'stairs_up', None), 'name') else getattr(room, 'stairs_up', None),
            'stairs_down': room.stairs_down.name if hasattr(getattr(room, 'stairs_down', None), 'name') else getattr(room, 'stairs_down', None)
        }
    
    def _serialize_item(self, item):
        return {
            'name': item.name,
            'description': item.description,
            'properties': {key: value for key, value in vars(item).items() 
                          if key not in ['name', 'description']}
        }
    
    def _serialize_npc(self, npc):
        return {
            'name': npc.name,
            'description': npc.description,
            'dialogue': npc.dialogue,
            'dialogue_data': getattr(npc, 'dialogue_data', {}),
            'inventory': [item.name for item in npc.inventory],
            'state': npc.state
        }

    def load_world(self) -> None:
        """Load and initialize the complete world"""
        try:
            # Load world configuration
            self._load_world_config()
            
            # Get world directory path
            world_path = self._get_world_path(self.world_id)
            
            # Initialize component loader
            self.component_loader = WorldComponentLoader(self)

            # Load all components (including puzzles)
            self.component_loader.load_components(world_path)
            
            # Verify room connections
            self._verify_room_connections()
            
        except Exception as e:
            self.logger.error(f"Failed to load world: {str(e)}")
            raise

    def _load_world_config(self) -> None:
        """Load world configuration from worlds.json"""
        try:
            config_path = self._get_config_path()
            with open(config_path) as f:
                worlds_data = json.load(f)
                world_data = worlds_data.get(self.world_id)
                if not world_data:
                    raise ValueError(f"No configuration found for world {self.world_id}")
                    
                self.config = GameWorldConfig(**world_data)
                self.name = self.config.name
                
        except Exception as e:
            self.logger.error(f"Failed to load world config: {str(e)}")
            raise

    def get_room(self, room_id: str) -> Optional[Room]:
        """Get a room by its ID"""
        normalized_id = self._normalize_room_id(room_id)
        return self.rooms.get(normalized_id)

    def get_starting_room(self) -> Optional[Room]:
        """Get the world's starting room"""
        if not self.config or not self.config.starting_room:
            return next(iter(self.rooms.values())) if self.rooms else None
            
        starting_room_id = self._normalize_room_id(self.config.starting_room)
        room = self.get_room(starting_room_id)
        
        if not room:
            self.logger.error(f"Starting room '{starting_room_id}' not found")
            return next(iter(self.rooms.values())) if self.rooms else None
            
        return room

    def _normalize_room_id(self, room_id: str) -> str:
        """Normalize room ID to standard format"""
        if not room_id:
            return ""
            
        # If room_id is a Room object, use its name
        if hasattr(room_id, 'name'):
            room_id = room_id.name
            
        # Convert to lowercase and replace spaces/apostrophes
        room_id = str(room_id).lower().replace(' ', '_').replace("'", '')
        
        # If it's already a full path (e.g. level_two/room_name), use it as is
        if '/' in room_id:
            return room_id
            
        # If we're in a room that has a level prefix, use that level
        if self.current_level:
            return f"{self.current_level}/{room_id}"
            
        # Default to level_one if we can't determine the level
        return f"level_one/{room_id}"

    def _verify_room_connections(self) -> None:
        """Verify all room connections are valid"""
        for room_id, room in self.rooms.items():
            # self.logger.debug(f"Verifying exits for room {room_id}")
            # Update current_level based on the room we're checking
            if '/' in room_id:
                self.current_level = room_id.split('/')[0]
            for exit_dir in room.exits():
                target_room = getattr(room, exit_dir)
                if not target_room:
                    self.logger.warning(f"Room {room_id} has invalid exit {exit_dir}")
                # else:
                #     self.logger.debug(f"  {exit_dir} -> {target_room}")

    @classmethod
    def load_all_worlds(cls) -> Dict[str, 'GameWorld']:
        """Load all available worlds"""
        worlds = {}
        config_path = cls._get_config_path()
        
        try:
            with open(config_path) as f:
                worlds_data = json.load(f)
                
            for world_id in worlds_data:
                try:
                    world = cls(world_id)
                    world.load_world()
                    worlds[world.name.lower()] = world
                    logging.info(f"Successfully loaded world: {world.name}")
                except Exception as e:
                    logging.error(f"Error loading world '{world_id}': {str(e)}")
                    # Continue loading other worlds
                    continue
                
            return worlds
            
        except Exception as e:
            logging.error(f"Failed to load worlds configuration: {str(e)}")
            raise

    @staticmethod
    def _get_config_path() -> Path:
        """Get path to worlds configuration file"""
        return Path(__file__).parent.parent.parent.parent / 'data' / 'worlds.json'

    @staticmethod
    def _get_world_path(world_id: str) -> Path:
        """Get path to world directory"""
        base_path = Path(__file__).parent.parent.parent.parent  # Go up to project root
        return base_path / 'data' / world_id.lower().replace(' ', '_')

    def get_item(self, item_id: str) -> Optional[Item]:
        """Get an item by ID."""
        return self.items.get(item_id)

    def get_npc(self, npc_id: str) -> Optional[NPC]:
        """Get an NPC by ID."""
        return self.npcs.get(npc_id)

    def get_puzzle(self, puzzle_id: str) -> Optional[BasePuzzle]:
        """Get a puzzle by ID."""
        return self.puzzles.get(puzzle_id)

    def get_all_rooms(self) -> List[Room]:
        """Get all rooms in the world."""
        return list(self.rooms.values())

    def get_all_items(self) -> List[Item]:
        """Get all items in the world."""
        return list(self.items.values())

    def get_all_npcs(self) -> List[NPC]:
        """Get all NPCs in the world."""
        return list(self.npcs.values())

    def get_all_puzzles(self) -> List[BasePuzzle]:
        """Get all puzzles in the world."""
        return list(self.puzzles.values())
