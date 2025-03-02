import json
import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import pickle
import traceback
import logging
from core.systems.ProgressionSystem import ProgressionSystem
from typing import Tuple

logger = logging.getLogger(__name__)

class GameState:
    def __init__(self, game):
        self.game = game
        self.saves_directory = Path("saves")
        self.saves_directory.mkdir(exist_ok=True)
        self.progression = ProgressionSystem(self)
        self.world_progress = self.progression.world_progress

    def serialize(self):
        return {
            'world_progress': self.world_progress,
            'saves_directory': str(self.saves_directory)
        }
    
    def deserialize(self, data):
        """Load game state from serialized data."""
        try:
            self.world_progress = data.get('world_progress', {})
            # Add any additional state restoration here
            return True
        except Exception as e:
            logger.error(f"Error deserializing game state: {str(e)}")
            return False

    def save_game(self, save_name: str) -> bool:
        """
        Save game state with custom name.  
        This now stores the player's current room ID in normalized form
        so it matches the keys in current_world.rooms exactly.
        """
        try:
            game = self.game
            saves_dir = self.saves_directory
            saves_dir.mkdir(exist_ok=True)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # Find the normalized key for the player's current room
            current_room_id = None
            if game.current_world and game.player.current_room:
                for r_id, r_obj in game.current_world.rooms.items():
                    if r_obj == game.player.current_room:
                        current_room_id = r_id
                        break

            # Build save state
            state = {
                'metadata': {
                    'save_name': save_name,
                    'timestamp': timestamp,
                    'version': '1.0'
                },
                'player': {
                    'inventory': [item.name for item in game.player.inventory],
                    'current_room': current_room_id,  # This is now the normalized ID
                    'visited_rooms': list(game.player.state.visited_rooms)
                },
                'world': {
                    'current_world': game.current_world.name if game.current_world else None,
                    'room_states': {
                        room_id: {
                            'items': [item.name for item in room.items]
                        }
                        for room_id, room in game.current_world.rooms.items()
                    } if game.current_world else {}
                },
                'puzzles': {
                    puzzle_id: {
                        'completed': puzzle.completed,
                        'completed_groups': list(getattr(puzzle, '_completed_groups', set()))
                    }
                    for puzzle_id, puzzle in game.current_world.puzzles.items()
                } if game.current_world else {},
                'progression': {
                    'world_progress': self.progression.world_progress
                }
            }

            # Save to file
            filename = f"{save_name}_{timestamp}.save"
            save_path = saves_dir / filename

            with open(save_path, 'wb') as f:
                pickle.dump(state, f)

            logger.info(f"Game saved successfully as '{save_name}'")
            return True

        except Exception as e:
            logger.error(f"Error saving game: {str(e)}")
            logger.error(traceback.format_exc())
            return False

    def load_game(self, save_name: str) -> bool:
        """
        Load game state from a named save.  
        Now also normalizes the saved room ID to avoid None-type current_room.
        If the normalized room is not found, fallback to the world's starting room.
        """
        try:
            # Find the most recent save file with this name
            save_files = list(self.saves_directory.glob(f"{save_name}_*.save"))
            if not save_files:
                logger.warning(f"No save file found with name '{save_name}'")
                return False

            # Get most recent save for this name
            save_path = max(save_files, key=lambda p: p.stat().st_mtime)

            with open(save_path, 'rb') as f:
                state = pickle.load(f)

            # Validate save data
            if not self._validate_save_data(state):
                logger.warning("Invalid save data structure")
                return False

            # Reset to initial state
            game = self.game
            game.setup()  # This sets up worlds, etc.

            # Restore world
            if state['world']['current_world']:
                # Find the matching loaded world name
                world_name = state['world']['current_world']
                if world_name in game.worlds:
                    game.current_world = game.worlds[world_name]
                    game.current_world.initialize(self)
                else:
                    logger.warning(f"World '{world_name}' not found among loaded worlds.")
                    return False

                # Restore inventory
                game.player.inventory.clear()
                for item_name in state['player']['inventory']:
                    for world_item in game.current_world.items.values():
                        if world_item.name == item_name:
                            game.player.inventory.add(world_item)
                            break

                # Restore room items
                for room_id, room_state in state['world']['room_states'].items():
                    if room_id in game.current_world.rooms:
                        room = game.current_world.rooms[room_id]
                        room.items.clear()
                        for item_name in room_state['items']:
                            for world_item in game.current_world.items.values():
                                if world_item.name == item_name:
                                    room.items.add(world_item)
                                    break

                # Restore current room (normalize if needed)
                saved_room_id = state['player']['current_room']

                if saved_room_id is not None:
                    # Attempt to see if it matches as-is
                    if saved_room_id not in game.current_world.rooms:
                        # If not, try the world's own normalization
                        normalized_id = game.current_world._normalize_room_id(saved_room_id)
                        if normalized_id in game.current_world.rooms:
                            saved_room_id = normalized_id
                        else:
                            # Fallback: use starting room
                            logger.warning(f"Room '{saved_room_id}' not found. Falling back to starting room.")
                            start_rm = game.current_world.get_starting_room()
                            game.player.current_room = start_rm
                            if start_rm is not None:
                                # We'll store the new ID to keep the player's state consistent
                                for r_id, r_obj in game.current_world.rooms.items():
                                    if r_obj == start_rm:
                                        game.player.state.current_room_id = r_id
                                        break
                            game.player.state.current_world_id = game.current_world.name
                            game.player.state.visited_rooms = set(state['player'].get('visited_rooms', []))
                            # Done with fallback
                            self._restore_puzzles(state)
                            # Successfully loaded with fallback:
                            logger.info(f"Game loaded successfully from '{save_name}' with fallback room.")
                            return True

                    # If still valid, set player's room on success
                    game.player.current_room = game.current_world.rooms[saved_room_id]
                    game.player.state.current_room_id = saved_room_id
                    game.player.state.current_world_id = state['world']['current_world']

                # Restore visited rooms
                game.player.state.visited_rooms = set(state['player'].get('visited_rooms', []))

                # Restore puzzle states
                self._restore_puzzles(state)

            logger.info(f"Game loaded successfully from '{save_name}'")
            return True

        except Exception as e:
            logger.error(f"Error loading game: {str(e)}")
            logger.error(traceback.format_exc())
            return False

    def list_saves(self) -> list:
        """List all available save files."""
        saves = []
        for save_file in self.saves_directory.glob("*.save"):
            try:
                with open(save_file, 'rb') as f:
                    save_data = pickle.load(f)
                    saves.append({
                        'name': save_data['metadata']['save_name'],
                        'timestamp': save_data['metadata']['timestamp'],
                        'filename': save_file.name
                    })
            except Exception:
                continue

        # Sort by timestamp, newest first
        return sorted(saves, key=lambda x: x['timestamp'], reverse=True)

    def _validate_save_data(self, state: Dict) -> bool:
        """Validate save data structure."""
        required_keys = ['metadata', 'player', 'world', 'puzzles', 'progression']
        if not all(key in state for key in required_keys):
            return False

        # Version check
        version = state['metadata'].get('version', '0')
        if version != '1.0':
            return False

        return True

    def delete_save(self, save_name: str) -> bool:
        """Delete a named save file."""
        try:
            save_files = list(self.saves_directory.glob(f"{save_name}_*.save"))
            for save_file in save_files:
                save_file.unlink()
            return True
        except Exception as e:
            logger.error(f"Error deleting save '{save_name}': {str(e)}")
            return False

    def delete_game_save(self, save_number: int) -> Tuple[bool, str]:
        """Delete a save game by its number in the list."""
        try:
            saves = self.list_saves()
            if not saves:
                return False, "No saves found."

            if not (1 <= save_number <= len(saves)):
                return False, "Invalid save number."

            save_to_delete = saves[save_number - 1]
            save_path = self.saves_directory / save_to_delete['filename']

            try:
                save_path.unlink()  # Delete the file
                return True, f"Deleted save: {save_to_delete['name']}"
            except FileNotFoundError:
                return False, "Save file not found."
            except Exception as e:
                logger.error(f"Error deleting save file: {str(e)}")
                return False, "Error deleting save file."

        except Exception as e:
            logger.error(f"Error in delete_game_save: {str(e)}")
            return False, "Error processing delete command."

    def _restore_puzzles(self, state: Dict[str, Any]) -> None:
        """Restore puzzle states from the save data."""
        # Restore puzzle completion
        if 'puzzles' not in state:
            return
        for puzzle_id, puzzle_state in state['puzzles'].items():
            if puzzle_id in self.game.current_world.puzzles:
                puzzle = self.game.current_world.puzzles[puzzle_id]
                puzzle.completed = puzzle_state.get('completed', False)
                if hasattr(puzzle, '_completed_groups'):
                    puzzle._completed_groups = set(puzzle_state.get('completed_groups', []))
                puzzle.game = self.game

        # Restore progression
        if 'progression' in state:
            self.progression.world_progress = state['progression']['world_progress']
            # If there's anything else needed for progression, do it here