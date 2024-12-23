from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle


class SpiritLevelPuzzle(BasePuzzle):
    puzzle_type = "spirit_level"
    
    def __init__(self):
        super().__init__(
            puzzle_id="spirit_level_puzzle",
            name="Trial of Spirit Force",
            description="Master the elements of spirit through ethereal resonance, astral ascension, and ancestral bonds",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "ethereal_resonance": {
                "room": "raavas_ethereal_sanctuary",
                "verbs": {
                    # Light manipulation
                    "attune",
                    "radiate",
                    "glow",
                    "shine",
                    "illuminate",
                    # Energy control
                    "pulse",
                    "resonate",
                    "harmonize",
                    "vibrate",
                    "channel",
                    # Spiritual actions
                    "connect",
                    "merge",
                    "transcend",
                    "unite",
                    "balance"
                },
                "nouns": {
                    # Light elements
                    "light",
                    "lights",
                    "ray",
                    "rays",
                    # Energy forms
                    "energy",
                    "energies",
                    "pulse",
                    "pulses",
                    # Spirit aspects
                    "spirit",
                    "spirits",
                    "essence",
                    "essences",
                    # Sanctuary elements
                    "sanctuary",
                    "sanctuaries",
                    "portal",
                    "portals",
                    # Ethereal aspects
                    "aura",
                    "auras",
                    "veil",
                    "veils"
                }
            },
            "astral_ascension": {
                "room": "celeste_mountains_astral_ascent",
                "verbs": {
                    # Astral movement
                    "project",
                    "soar",
                    "float",
                    "ascend",
                    "drift",
                    # Mental actions
                    "dream",
                    "envision",
                    "imagine",
                    "perceive",
                    "contemplate",
                    # Spiritual travel
                    "traverse",
                    "journey",
                    "explore",
                    "transcend",
                    "navigate"
                },
                "nouns": {
                    # Celestial bodies
                    "star",
                    "stars",
                    "moon",
                    "moons",
                    # Mental realms
                    "realm",
                    "realms",
                    "dream",
                    "dreams",
                    # Vision aspects
                    "vision",
                    "visions",
                    "sight",
                    "sights",
                    # Spiritual elements
                    "soul",
                    "souls",
                    "mind",
                    "minds",
                    # Path elements
                    "path",
                    "paths",
                    "bridge",
                    "bridges"
                }
            },
            "ancestral_bonds": {
                "room": "mount_pyres_ancestral_summit",
                "verbs": {
                    # Connection actions
                    "honor",
                    "connect",
                    "bond",
                    "link",
                    "unite",
                    # Communication
                    "whisper",
                    "speak",
                    "pray",
                    "chant",
                    "call",
                    # Memory actions
                    "remember",
                    "recall",
                    "revere",
                    "reflect",
                    "preserve"
                },
                "nouns": {
                    # Ancestor aspects
                    "ancestor",
                    "ancestors",
                    "spirit",
                    "spirits",
                    # Memory elements
                    "memory",
                    "memories",
                    "story",
                    "stories",
                    # Sacred spaces
                    "shrine",
                    "shrines",
                    "altar",
                    "altars",
                    # Connection aspects
                    "bond",
                    "bonds",
                    "voice",
                    "voices",
                    # Mountain features
                    "mist",
                    "mists",
                    "peak",
                    "peaks"
                }
            }
        }

    def handle_command(self, command: str, room_id: str, inventory: List[str]) -> Tuple[bool, str]:
        """
        Attempt to solve a piece of the spirit mastery puzzle by typing commands such as:
        'attune light' in Raava's Sanctuary, 'project realm' in Celeste Mountains, 
        'honor ancestor' at Mount Pyres, etc.
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
                    return True, f"The spirits respond to your command. The {aspect.replace('_',' ')} grows stronger."

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
            return True, "The spirits resonate in harmony as ethereal, astral, and ancestral forces unite, opening a mystical path through the veil!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "raavas_ethereal_sanctuary",
            "celeste_mountains_astral_ascent",
            "mount_pyres_ancestral_summit"
        ])