from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle


class WaterLevelPuzzle(BasePuzzle):
    puzzle_type = "water_level"
    
    def __init__(self):
        super().__init__(
            puzzle_id="water_mastery_puzzle",
            name="Trial of Tidal Force",
            description="Master the elements of water through healing arts, ocean wisdom, and playful mastery",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "healing_arts": {
                "room": "kataras_waterbending_rapids",
                "verbs": {
                    # Core healing
                    "heal",
                    "mend",
                    "restore",
                    "soothe",
                    "cleanse",
                    # Water control
                    "flow",
                    "bend",
                    "guide",
                    "shape",
                    "direct",
                    # Energy work
                    "channel",
                    "focus",
                    "balance",
                    "purify",
                    "harmonize"
                },
                "nouns": {
                    # Healing elements
                    "spirit",
                    "spirits",
                    "wound",
                    "wounds",
                    # Water forms
                    "water",
                    "waters",
                    "stream",
                    "streams",
                    # Energy aspects
                    "energy",
                    "energies",
                    "essence",
                    "essences",
                    # Environment
                    "rapid",
                    "rapids",
                    "pool",
                    "pools",
                    # Moon aspects
                    "moon",
                    "moons",
                    "crystal",
                    "crystals"
                }
            },
            "ocean_wisdom": {
                "room": "moana_waves",
                "verbs": {
                    # Navigation
                    "navigate",
                    "guide",
                    "read",
                    "sail",
                    "chart",
                    # Connection
                    "listen",
                    "feel",
                    "sense",
                    "connect",
                    "attune",
                    # Understanding
                    "learn",
                    "understand",
                    "merge",
                    "embrace",
                    "know"
                },
                "nouns": {
                    # Ocean elements
                    "wave",
                    "waves",
                    "tide",
                    "tides",
                    # Navigation tools
                    "star",
                    "stars",
                    "current",
                    "currents",
                    # Sacred items
                    "heart",
                    "hearts",
                    "pendant",
                    "pendants",
                    # Ocean features
                    "reef",
                    "reefs",
                    "depth",
                    "depths",
                    # Celestial guides
                    "light",
                    "lights",
                    "path",
                    "paths"
                }
            },
            "playful_mastery": {
                "room": "squirtles_surfing_coast",
                "verbs": {
                    # Water play
                    "splash",
                    "play",
                    "dive",
                    "swim",
                    "float",
                    # Surfing moves
                    "ride",
                    "glide",
                    "surf",
                    "balance",
                    "spin",
                    # Trick moves
                    "flip",
                    "twist",
                    "jump",
                    "leap",
                    "dance"
                },
                "nouns": {
                    # Equipment
                    "board",
                    "boards",
                    "shell",
                    "shells",
                    # Wave types
                    "wave",
                    "waves",
                    "surf",
                    "surfs",
                    # Water features
                    "foam",
                    "foams",
                    "spray",
                    "sprays",
                    # Beach elements
                    "beach",
                    "beaches",
                    "coast",
                    "coasts",
                    # Water effects
                    "splash",
                    "splashes",
                    "ripple",
                    "ripples"
                }
            }
        }

    def handle_command(self, command: str, room_id: str, inventory: List[str]) -> Tuple[bool, str]:
        """
        Attempt to solve a piece of the water mastery puzzle by typing commands such as:
        'heal spirit' in Katara's Rapids, 'read tide' in Moana's Waves, 
        'ride surf' at Squirtle's Coast, etc.
        """
        if not self.is_puzzle_room(room_id):
            return False, "This puzzle cannot be advanced here."

        words = command.lower().split()
        if len(words) < 2:
            return False, "That doesn't seem to help."

        verb = words[0]
        noun = words[-1]

        for aspect, data in self.aspects.items():
            if aspect in self._completed_groups:
                continue

            if data["room"] in room_id.lower():
                if verb in data["verbs"] and noun in data["nouns"]:
                    self._completed_groups.add(aspect)
                    completed, msg = self._handle_completion()
                    if completed:
                        return True, msg
                    return True, f"The waters respond to your command. The {aspect.replace('_',' ')} flows stronger."

        return False, "Nothing happens."

    def _handle_completion(self) -> Tuple[bool, str]:
        """Check if all aspects are completed and handle completion."""
        if len(self._completed_groups) == len(self.aspects):
            self.completed = True
            if hasattr(self.game, 'game_state') and hasattr(self.game.game_state, 'progression'):
                self.game.game_state.progression.handle_puzzle_completion(
                    self.game.current_world.name, 
                    self.puzzle_id
                )
            return True, "The waters surge with harmony as healing, wisdom, and play unite, opening a serene path through the waves!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "kataras_waterbending_rapids",
            "moana_waves",
            "squirtles_surfing_coast"
        ])