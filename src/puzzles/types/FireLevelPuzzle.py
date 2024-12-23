from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle


class FireLevelPuzzle(BasePuzzle):
    puzzle_type = "fire_level"
    
    def __init__(self):
        super().__init__(
            puzzle_id="fire_mastery_puzzle",
            name="Trial of Fire Force",
            description="Master the elements of fire through pyromantic combat, dragon wisdom, and disciplined breath",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "pyromantic_combat": {
                "room": "chandras_flame_sanctuary",
                "verbs": {
                    # Core fire control
                    "channel",
                    "blast",
                    "surge",
                    "focus",
                    "ignite",
                    # Combat actions
                    "strike",
                    "attack",
                    "defend",
                    "dodge",
                    "counter",
                    # Energy manipulation
                    "direct",
                    "control",
                    "shape",
                    "release",
                    "harness"
                },
                "nouns": {
                    # Fire elements
                    "flame",
                    "flames",
                    "fire",
                    "fires",
                    # Combat elements
                    "inferno",
                    "infernos",
                    "blast",
                    "blasts",
                    # Energy forms
                    "power",
                    "powers",
                    "energy",
                    "energies",
                    # Battle aspects
                    "arena",
                    "arenas",
                    "rune",
                    "runes",
                    # Magical effects
                    "spark",
                    "sparks",
                    "blaze",
                    "blazes"
                }
            },
            "dragon_wisdom": {
                "room": "irohs_dragon_tea_garden",
                "verbs": {
                    # Tea ceremony
                    "steep",
                    "pour",
                    "brew",
                    "serve",
                    "drink",
                    # Meditation
                    "breathe",
                    "meditate",
                    "reflect",
                    "contemplate",
                    "center",
                    # Dragon teachings
                    "learn",
                    "understand",
                    "observe",
                    "sense",
                    "harmonize"
                },
                "nouns": {
                    # Tea elements
                    "tea",
                    "teas",
                    "leaf",
                    "leaves",
                    # Dragon aspects
                    "dragon",
                    "dragons",
                    "scale",
                    "scales",
                    # Garden features
                    "garden",
                    "gardens",
                    "statue",
                    "statues",
                    # Wisdom aspects
                    "wisdom",
                    "wisdoms",
                    "teaching",
                    "teachings",
                    # Spiritual elements
                    "spirit",
                    "spirits",
                    "breath",
                    "breaths"
                }
            },
            "disciplined_breath": {
                "room": "zukos_dragon_fire",
                "verbs": {
                    # Movement control
                    "flow",
                    "guide",
                    "balance",
                    "shift",
                    "align",
                    # Energy work
                    "channel",
                    "focus",
                    "direct",
                    "control",
                    "regulate",
                    # Training actions
                    "practice",
                    "train",
                    "perfect",
                    "master",
                    "study"
                },
                "nouns": {
                    # Energy concepts
                    "chi",
                    "chis",
                    "energy",
                    "energies",
                    # Training elements
                    "stance",
                    "stances",
                    "form",
                    "forms",
                    # Physical aspects
                    "heat",
                    "heats",
                    "breath",
                    "breaths",
                    # Training grounds
                    "ground",
                    "grounds",
                    "volcano",
                    "volcanos",
                    # Equipment
                    "sword",
                    "swords",
                    "blade",
                    "blades"
                }
            }
        }

    def handle_command(self, command: str, room_id: str, inventory: List[str]) -> Tuple[bool, str]:
        """
        Attempt to solve a piece of the fire mastery puzzle by typing commands such as:
        'channel flame' in Chandra's Sanctuary, 'steep tea' in Iroh's Garden, 
        'flow chi' in Zuko's Fire, etc.
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
                    return True, f"The flames respond to your command. The {aspect.replace('_',' ')} burns stronger."

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
            return True, "The fires roar in harmony as combat, wisdom, and discipline unite, opening a blazing path through the flames!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "chandras_flame_sanctuary",
            "irohs_dragon_tea_garden",
            "zukos_dragon_fire"
        ])