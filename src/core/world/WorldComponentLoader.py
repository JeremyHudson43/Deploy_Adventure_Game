import logging
from pathlib import Path
from typing import Optional
import traceback

from core.loaders.GameDataParser import GameDataParser
from core.loaders.GameEntityFactory import GameEntityFactory
from core.loaders.RoomConnectionManager import RoomConnectionManager
from puzzles.types.AirLevelPuzzle import AirLevelPuzzle
from puzzles.types.EarthLevelPuzzle import EarthLevelPuzzle
from puzzles.types.WaterLevelPuzzle import WaterLevelPuzzle
from puzzles.types.FireLevelPuzzle import FireLevelPuzzle
from puzzles.types.AlternativeRockPuzzle import AlternativeRockPuzzle
from puzzles.types.CreativeConvergencePuzzle import CreativeConvergencePuzzle
from puzzles.types.ChiptunePuzzle import ChiptunePuzzle
from puzzles.types.SteampunkMusicPuzzle import SteampunkMusicPuzzle
from puzzles.types.SpiritLevelPuzzle import SpiritLevelPuzzle
from puzzles.types.NostalgiaPuzzle import NostalgiaPuzzle

logger = logging.getLogger(__name__)

class WorldComponentLoader:
    def __init__(self, world):
        self.world = world
        self.json_loader = GameDataParser()
        self.creator = GameEntityFactory(world)
        self.connector = RoomConnectionManager(world)

    def load_components(self, world_path: Path) -> None:
        """Load all world components."""
        try:
            # First load all standard components
            self._load_standard_components(world_path)
            
            # Then set up room connections
            self.connector.setup_room_connections(world_path)
            
            # Finally load built-in puzzles
            self._load_built_in_puzzles()
            
        except Exception as e:
            logger.error(f"Error loading components: {str(e)}")
            raise

    def _load_standard_components(self, world_path: Path) -> None:
        """Load all JSON-based components."""
        try:
            # Load global components first
            self._load_global_components(world_path)

            # Then load level-specific components
            level_dirs = self.json_loader.get_level_dirs(world_path)
            for level_dir in level_dirs:
                self._load_level_components(level_dir)
                
        except Exception as e:
            logger.error(f"Error loading standard components: {e}")
            raise

    def _load_global_components(self, world_path: Path) -> None:
        """Load components from the world's root directory."""
        # Load global items
        items_path = world_path / 'items'
        if items_path.exists():
            for item_file in items_path.glob('*.json'):
                self.creator.create_item(item_file)
        
        # Load global NPCs
        npcs_path = world_path / 'npcs'
        if npcs_path.exists():
            for npc_file in npcs_path.glob('*.json'):
                self.creator.create_npc(npc_file)
        
        # Load global rooms
        rooms_path = world_path / 'rooms'
        if rooms_path.exists():
            for room_file in rooms_path.glob('*.json'):
                self.creator.create_room(room_file)

    def _load_level_components(self, level_dir: Path) -> None:
        """Load components from a specific level directory."""
        level = level_dir.name
        
        # Load level items
        items_path = level_dir / 'items'
        if items_path.exists():
            for item_file in items_path.glob('*.json'):
                self.creator.create_item(item_file, level=level)
        
        # Load level NPCs
        npcs_path = level_dir / 'npcs'
        if npcs_path.exists():
            for npc_file in npcs_path.glob('*.json'):
                self.creator.create_npc(npc_file, level=level)
        
        # Load level rooms
        rooms_path = level_dir / 'rooms'
        if rooms_path.exists():
            for room_file in rooms_path.glob('*.json'):
                self.creator.create_room(room_file, level=level)

    def _load_built_in_puzzles(self) -> None:
        """Initialize and load built-in Python puzzles based on world type."""
        logger.info(f"Loading built-in puzzles for world: {self.world.name}")
        
        if "Elemental Conflux" in self.world.name:
            self._load_elemental_puzzles()
        elif "Whimsical Realm" in self.world.name:
            self._load_whimsical_puzzles()
        elif "Harmonic Nexus" in self.world.name:
            self._load_harmonic_puzzles()
        
        logger.info(f"Finished loading puzzles. Available puzzles: {list(self.world.puzzles.keys())}")

    def _load_elemental_puzzles(self) -> None:
        """Load puzzles for Elemental Conflux world."""
        try:
            # Initialize Air puzzle
            air_puzzle = AirLevelPuzzle()
            
            # Initialize Earth puzzle
            earth_puzzle = EarthLevelPuzzle()
            
            # Initialize Water puzzle
            water_puzzle = WaterLevelPuzzle()
            
            # Initialize Fire puzzle
            fire_puzzle = FireLevelPuzzle()
            
            # Set up game references
            if hasattr(self.world, 'game_state') and hasattr(self.world.game_state, 'game'):
                air_puzzle.game = self.world.game_state.game
                earth_puzzle.game = self.world.game_state.game
                water_puzzle.game = self.world.game_state.game
                fire_puzzle.game = self.world.game_state.game
            
            # Add to world's puzzles
            self.world.puzzles[air_puzzle.puzzle_id] = air_puzzle
            self.world.puzzles[earth_puzzle.puzzle_id] = earth_puzzle
            self.world.puzzles[water_puzzle.puzzle_id] = water_puzzle
            self.world.puzzles[fire_puzzle.puzzle_id] = fire_puzzle
            
        except Exception as e:
            logger.error(f"Error loading Elemental puzzles: {e}")
            logger.error(traceback.format_exc())

    def _load_whimsical_puzzles(self) -> None:
        """Load puzzles for Whimsical Realm world."""
        try:
            # Initialize all puzzles
            alternative_rock = AlternativeRockPuzzle()
            creative_convergence = CreativeConvergencePuzzle()
            chiptune = ChiptunePuzzle()
            steampunk = SteampunkMusicPuzzle()
            spirit = SpiritLevelPuzzle()
            nostalgia = NostalgiaPuzzle()
            
            # Set up game references
            if hasattr(self.world, 'game_state') and hasattr(self.world.game_state, 'game'):
                alternative_rock.game = self.world.game_state.game
                creative_convergence.game = self.world.game_state.game
                chiptune.game = self.world.game_state.game
                steampunk.game = self.world.game_state.game
                spirit.game = self.world.game_state.game
                nostalgia.game = self.world.game_state.game
            
            # Add to world's puzzles
            self.world.puzzles[alternative_rock.puzzle_id] = alternative_rock
            self.world.puzzles[creative_convergence.puzzle_id] = creative_convergence
            self.world.puzzles[chiptune.puzzle_id] = chiptune
            self.world.puzzles[steampunk.puzzle_id] = steampunk
            self.world.puzzles[spirit.puzzle_id] = spirit
            self.world.puzzles[nostalgia.puzzle_id] = nostalgia
        
        except Exception as e:
            logger.error(f"Error loading Whimsical puzzles: {e}")
            logger.error(traceback.format_exc())

    def _load_harmonic_puzzles(self) -> None:
        """Load puzzles for Harmonic Nexus world."""
        try:
            # Initialize all puzzles
            alternative_rock = AlternativeRockPuzzle()
            chiptune = ChiptunePuzzle()
            steampunk = SteampunkMusicPuzzle()
            
            # Set up game references
            if hasattr(self.world, 'game_state') and hasattr(self.world.game_state, 'game'):
                alternative_rock.game = self.world.game_state.game
                chiptune.game = self.world.game_state.game
                steampunk.game = self.world.game_state.game
            
            # Add to world's puzzles
            self.world.puzzles[alternative_rock.puzzle_id] = alternative_rock
            self.world.puzzles[chiptune.puzzle_id] = chiptune
            self.world.puzzles[steampunk.puzzle_id] = steampunk
            
        except Exception as e:
            logger.error(f"Error loading Harmonic puzzles: {e}")
            logger.error(traceback.format_exc())