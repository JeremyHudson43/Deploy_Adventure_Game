"""
Handles level progression and unlocking in the game.
"""

import re
from typing import Dict, Optional

class ProgressionSystem:
    def __init__(self, game_state):
        self.game_state = game_state
        self.world_progress: Dict[str, Dict] = {
            "Elemental Conflux": {"unlocked_level": 1},
            "Harmonic Nexus": {"unlocked_level": 1},
            "Whimsical Realm": {"unlocked_level": 1}
        }
        self._load_progress()
        self.dev_mode = False

    def _load_progress(self):
        """Load progress from game state if it exists."""
        if hasattr(self.game_state, 'world_progress'):
            self.world_progress = self.game_state.world_progress

    def _save_progress(self):
        """Save progress to game state."""
        self.game_state.world_progress = self.world_progress
        if hasattr(self.game_state, 'save_state'):
            self.game_state.save_state()

    def get_level_number(self, room_id: str) -> Optional[int]:
        """Extract level number from room ID."""
        if not isinstance(room_id, str):
            if hasattr(room_id, 'id'):
                room_id = room_id.id
            else:
                return None
            
        level_match = re.match(r"level_(\w+)/", room_id)
        if not level_match:
            return None
            
        level_word = level_match.group(1)
        number_map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        return number_map.get(level_word.lower())

    def is_room_accessible(self, world_name: str, room_id: str) -> bool:
        """Check if a room is accessible based on current progression."""
        if self.dev_mode:
            return True
            
        level_num = self.get_level_number(room_id)
        if level_num is None:
            return True  # Non-level rooms are always accessible
            
        unlocked_level = self.world_progress.get(world_name, {}).get("unlocked_level", 1)
        return level_num <= unlocked_level

    def unlock_next_level(self, world_name: str) -> bool:
        """Unlock the next level in a world."""
        if world_name not in self.world_progress:
            self.world_progress[world_name] = {"unlocked_level": 1}
            
        current_level = self.world_progress[world_name]["unlocked_level"]
        self.world_progress[world_name]["unlocked_level"] = current_level + 1
        self._save_progress()
        return True

    def get_unlocked_level(self, world_name: str) -> int:
        """Get the highest unlocked level for a world."""
        return self.world_progress.get(world_name, {}).get("unlocked_level", 1)

    def toggle_dev_mode(self, keyword: str) -> bool:
        """Toggle dev mode with a special keyword."""
        if keyword == "florbglorbule":
            self.dev_mode = True
            return True
        return False

    def handle_puzzle_completion(self, world_name: str, puzzle_id: str) -> None:
        """Handle puzzle completion by unlocking the next level."""
        # Define puzzle sequences for each world
        world_puzzle_sequences = {
            "Elemental Conflux": {
                "air_currents_puzzle": 1,      # Air Level unlocks Earth
                "earth_stability_puzzle": 2,    # Earth Level unlocks Fire
                "fire_mastery_puzzle": 3,     # Fire Level unlocks Water
                "water_mastery_puzzle": 4,         # Water Level unlocks Spirit
                "spirit_level_puzzle": 5      # Spirit Level (final)
            },
            "Harmonic Nexus": {
                "alternative_rock_puzzle": 1,    # Alternative Rock unlocks Creative
                "chiptune_puzzle": 2,           # Chiptune unlocks Steampunk
                "steampunk_harmonic_puzzle": 3,    # Steampunk unlocks Retro
            },
            "Whimsical Realm": {
                "nostalgia_puzzle": 1,          # Level 1: Bob Ross Haven & friends
                "creative_convergence_puzzle": 2,         # Level 2: Mad Hatter & Queen of Hearts
                "childhood_puzzle": 3           # Level 3: Brave Little Toaster & friends
            }
        }
        
        # Get the puzzle sequence for the current world
        puzzle_sequence = world_puzzle_sequences.get(world_name, {})
        
        if puzzle_id in puzzle_sequence:
            current_level = puzzle_sequence[puzzle_id]
            max_level = max(puzzle_sequence.values())
            if current_level < max_level:  # Don't increment past the final level
                self.unlock_next_level(world_name)