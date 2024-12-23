# src/save_system/game_state.py

import json
from pathlib import Path
import datetime
from typing import Dict, Optional, Any
from core.systems.ProgressionSystem import ProgressionSystem

class GameState:
    def __init__(self, game):
        self.game = game
        self.saves_directory = Path("saves")
        self.saves_directory.mkdir(exist_ok=True)
        self.progression = ProgressionSystem(self)
        self.world_progress = self.progression.world_progress

    def save_game(self, slot: str = "quicksave") -> bool:
        """
        Save the current game state to a file.
        
        Args:
            slot: Save slot name (default: "quicksave")
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_data = {
                "metadata": {
                    "timestamp": timestamp,
                    "version": "1.0",
                    "slot": slot
                },
                "player_state": self._serialize_player(),
                "world_state": self._serialize_world_state(),
                "puzzle_state": self._serialize_puzzle_state(),
                "world_progress": self.world_progress
            }

            # Create filename with timestamp
            filename = f"{slot}_{timestamp}.json"
            save_path = self.saves_directory / filename

            # Save the file
            with open(save_path, "w", encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            # Cleanup old saves if quicksave
            if slot == "quicksave":
                self._cleanup_old_quicksaves()

            self.game.display.print_message(f"Game saved successfully to slot: {slot}")
            return True

        except Exception as e:
            self.game.display.print_message(f"Error saving game: {str(e)}")
            return False

    def load_game(self, slot: str = "quicksave") -> bool:
        """
        Load a game state from a file.
        
        Args:
            slot: Save slot to load from (default: "quicksave")
            
        Returns:
            bool: True if load was successful, False otherwise
        """
        try:
            # Find the most recent save file for the given slot
            save_files = list(self.saves_directory.glob(f"{slot}_*.json"))
            if not save_files:
                self.game.display.print_simple_message(f"No saved game found in slot: {slot}")
                return False

            # Get the most recent save file
            save_path = max(save_files, key=lambda p: p.stat().st_mtime)

            # Load and validate save data
            with open(save_path, "r", encoding='utf-8') as f:
                save_data = json.load(f)

            if not self._validate_save_data(save_data):
                self.game.display.print_simple_message("Warning: This save file appears to be corrupted or from a different version")
                return False

            # Restore game state
            self._deserialize_player(save_data["player_state"])
            self._deserialize_world_state(save_data["world_state"])
            self._deserialize_puzzle_state(save_data["puzzle_state"])
            self.world_progress = save_data.get("world_progress", self.progression.world_progress)
            self.progression.world_progress = self.world_progress

            self.game.display.print_message(f"Game loaded successfully from slot: {slot}")
            return True

        except Exception as e:
            self.game.display.print_message(f"Error loading game: {str(e)}")
            return False

    def list_saves(self) -> list:
        """List all available save slots with their timestamps."""
        saves = []
        for save_file in self.saves_directory.glob("*.json"):
            try:
                with open(save_file, "r", encoding='utf-8') as f:
                    save_data = json.load(f)
                    saves.append({
                        "slot": save_data["metadata"]["slot"],
                        "timestamp": save_data["metadata"]["timestamp"],
                        "filename": save_file.name
                    })
            except Exception:
                continue
        return saves

    def _serialize_player(self) -> Dict[str, Any]:
        """Serialize player state."""
        return {
            "current_room": self.game.player.current_room.name,
            "inventory": [item.name for item in self.game.player.inventory],
            "position": {
                "world": self.game.current_world.name,
                "room": self.game.player.current_room.name
            }
        }

    def _serialize_world_state(self) -> Dict[str, Any]:
        """Serialize current world state."""
        return {
            "current_world": self.game.current_world.name,
            "rooms": {
                room_id: {
                    "items": [item.name for item in room.items],
                    "npcs": [npc.name for npc in getattr(room, 'npcs', [])]
                }
                for room_id, room in self.game.current_world.rooms.items()
            }
        }

    def _serialize_puzzle_state(self) -> Dict[str, Any]:
        """Serialize puzzle states."""
        puzzle_state = {}
        if hasattr(self.game.current_world, 'puzzles'):
            for puzzle_id, puzzle in self.game.current_world.puzzles.items():
                puzzle_state[puzzle_id] = {
                    "completed": puzzle.completed,
                    "state": getattr(puzzle, 'sequence_state', None),
                    "visited_worlds": list(getattr(puzzle, 'visited_worlds', set()))
                }
        return puzzle_state

    def _deserialize_player(self, player_data: Dict[str, Any]) -> None:
        """Restore player state."""
        # Switch to correct world first
        world_name = player_data["position"]["world"]
        if world_name in self.game.worlds:
            self.game.current_world = self.game.worlds[world_name]
            
        # Restore room position
        room_name = player_data["position"]["room"]
        if room_name in self.game.current_world.rooms:
            self.game.player.current_room = self.game.current_world.rooms[room_name]
            
        # Restore inventory
        self.game.player.inventory.clear()
        for item_name in player_data["inventory"]:
            for item in self.game.current_world.items.values():
                if item.name == item_name:
                    self.game.player.inventory.add(item)
                    break

    def _deserialize_world_state(self, world_data: Dict[str, Any]) -> None:
        """Restore world state."""
        for room_id, room_data in world_data["rooms"].items():
            if room_id in self.game.current_world.rooms:
                room = self.game.current_world.rooms[room_id]
                # Restore items
                room.items.clear()
                for item_name in room_data["items"]:
                    for item in self.game.current_world.items.values():
                        if item.name == item_name:
                            room.items.add(item)
                            break

    def _deserialize_puzzle_state(self, puzzle_data: Dict[str, Any]) -> None:
        """Restore puzzle states."""
        if hasattr(self.game.current_world, 'puzzles'):
            for puzzle_id, puzzle_state in puzzle_data.items():
                if puzzle_id in self.game.current_world.puzzles:
                    puzzle = self.game.current_world.puzzles[puzzle_id]
                    puzzle.completed = puzzle_state["completed"]
                    if puzzle_state["state"]:
                        puzzle.sequence_state = puzzle_state["state"]
                    if puzzle_state["visited_worlds"]:
                        puzzle.visited_worlds = set(puzzle_state["visited_worlds"])

    def _validate_save_data(self, save_data: Dict[str, Any]) -> bool:
        """Validate save data structure and version compatibility."""
        required_keys = ["metadata", "player_state", "world_state", "puzzle_state"]
        if not all(key in save_data for key in required_keys):
            return False
        
        # Version check
        version = save_data["metadata"].get("version", "0")
        if version != "1.0":  # Current version
            return False
            
        return True

    def _cleanup_old_quicksaves(self, keep_count: int = 5) -> None:
        """Keep only the most recent quicksaves."""
        quicksaves = list(self.saves_directory.glob("quicksave_*.json"))
        if len(quicksaves) > keep_count:
            # Sort by modification time, oldest first
            quicksaves.sort(key=lambda p: p.stat().st_mtime)
            # Remove older files
            for save_file in quicksaves[:-keep_count]:
                save_file.unlink()