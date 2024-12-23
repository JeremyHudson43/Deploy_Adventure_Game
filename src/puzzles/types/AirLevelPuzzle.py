from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle


class AirLevelPuzzle(BasePuzzle):
    puzzle_type = "air_level"
    
    def __init__(self):
        super().__init__(
            puzzle_id="air_currents_puzzle",
            name="Trial of Wind Mastery",
            description="A multi-part challenge requiring spiritual harmony, celestial navigation, and storm communion to master the winds.",
            puzzle_type=self.puzzle_type
        )

        self._completed_groups = set()

        self.aspects = {
            "spiritual_harmony": {
                "room": "aangs_airbending_academy",
                "verbs": {
                    # Core spiritual actions
                    "focus",
                    "breathe",
                    "sense",
                    "feel",
                    "meditate",
                    # Learning-related actions
                    "observe",
                    "study",
                    "guide",
                    "channel",
                    "stir",
                    # Additional spiritual verbs
                    "flow",
                    "harmonize",
                    "balance",
                    "center",
                    "attune"
                },
                "nouns": {
                    # From Wind Resonance Crystals
                    "crystal",
                    "crystals",
                    # From room atmosphere
                    "breeze",
                    "breezes",
                    # From crystal properties
                    "resonance",
                    "resonances",
                    # From air movements
                    "current",
                    "currents",
                    # From airbending practice
                    "breath",
                    "breaths",
                    # Core element
                    "wind",
                    "winds",
                    # Spiritual aspect
                    "spirit",
                    "spirits",
                    # From room description
                    "scroll",
                    "scrolls",
                    "chime",
                    "chimes",
                    # Navigation element
                    "path",
                    "paths"
                }
            },
            "celestial_navigation": {
                "room": "marios_wing_cap_heights",
                "verbs": {
                    # Movement verbs
                    "align",
                    "trace",
                    "follow",
                    "tune",
                    "dance",
                    # Flight verbs
                    "soar",
                    "glide",
                    "float",
                    "hover",
                    "fly",
                    # Additional movement
                    "leap",
                    "dive",
                    "ascend",
                    "navigate",
                    "drift"
                },
                "nouns": {
                    # From Power Star
                    "star",
                    "stars",
                    # From environment
                    "cloud",
                    "clouds",
                    # Navigation element
                    "path",
                    "paths",
                    # From room structure
                    "platform",
                    "platforms",
                    # From Wing Cap
                    "cap",
                    "caps",
                    # From Power Star
                    "power",
                    "powers",
                    # From Wing Cap
                    "wing",
                    "wings",
                    # From location name
                    "height",
                    "heights",
                    # From environment
                    "sky",
                    "skies",
                    # From star glow
                    "light",
                    "lights"
                }
            },
            "storm_communion": {
                "room": "storm_crows_ascension",
                "verbs": {
                    # Basic interactions
                    "channel",
                    "guide",
                    "stir",
                    "hear",
                    "touch",
                    # Control actions
                    "control",
                    "harness",
                    "calm",
                    "direct",
                    "focus",
                    # Storm effects
                    "surge",
                    "crackle",
                    "flash",
                    "rumble",
                    "echo"
                },
                "nouns": {
                    # Storm elements
                    "thunder",
                    "thunders",
                    "lightning",
                    "lightnings",
                    # Storm types
                    "tempest",
                    "tempests",
                    "storm",
                    "storms",
                    # From NPC
                    "crow",
                    "crows",
                    # From items
                    "feather",
                    "feathers",
                    "rod",
                    "rods",
                    # Environment
                    "cloud",
                    "clouds",
                    "spire",
                    "spires",
                    # From magical effects
                    "energy",
                    "energies"
                }
            }
        }

    def handle_command(self, command: str, room_id: str, inventory: List[str]) -> Tuple[bool, str]:
        """
        Attempt to solve a piece of the air currents puzzle by typing commands such as:
        'focus crystal' in Aang's Academy, 'align stars' in Mario's Heights, 
        'channel thunder' in the Storm Crow's Ascension, etc.
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
                    return True, f"The air currents shift in response. The {aspect.replace('_',' ')} grows stronger."

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
            return True, "The combined powers of air currents, celestial navigation, and storm energy create a path forward!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "aangs_airbending_academy",
            "marios_wing_cap_heights",
            "storm_crows_ascension"
        ])
