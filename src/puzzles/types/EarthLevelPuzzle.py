from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
from puzzles.core.GenericPuzzleBase import GenericPuzzleBase

class EarthLevelPuzzle(GenericPuzzleBase):
    puzzle_type = "earth_level"
    
    def __init__(self):
        super().__init__(
            puzzle_id="earth_stability_puzzle",
            name="Trial of Earth Force",
            description="Master the elements of earth through seismic resonance, tactical earthbending, and forge mastery",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "seismic_resonance": {
                "room": "tophs_crystal_caverns",
                "verbs": {
                    # Core sensing actions
                    "sense",
                    "listen",
                    "feel",
                    "attune",
                    "focus",
                    # Crystal manipulation
                    "resonate",
                    "pulse",
                    "hum",
                    "vibrate",
                    "glow",
                    # Earth manipulation
                    "bend",
                    "shape",
                    "shift",
                    "mold",
                    "form"
                },
                "nouns": {
                    # Core materials
                    "crystal",
                    "crystals",
                    "earth",
                    "earths",
                    # Ground elements
                    "stone",
                    "stones",
                    "ground",
                    "grounds",
                    # Sensory elements
                    "vibration",
                    "vibrations",
                    "resonance",
                    "resonances",
                    # Cave features
                    "cavern",
                    "caverns",
                    "formation",
                    "formations",
                    # Energy aspects
                    "energy",
                    "energies",
                    "force",
                    "forces"
                }
            },
            "tactical_earthbending": {
                "room": "rock_solid_chess_dojo",
                "verbs": {
                    # Chess moves
                    "move",
                    "position",
                    "advance",
                    "capture",
                    "defend",
                    # Combat actions
                    "strike",
                    "block",
                    "counter",
                    "train",
                    "spar",
                    # Strategy
                    "plan",
                    "calculate",
                    "analyze",
                    "study",
                    "observe"
                },
                "nouns": {
                    # Chess pieces
                    "piece",
                    "pieces",
                    "pawn",
                    "pawns",
                    # Board elements
                    "board",
                    "boards",
                    "square",
                    "squares",
                    # Combat terms
                    "stance",
                    "stances",
                    "form",
                    "forms",
                    # Strategic elements
                    "strategy",
                    "strategies",
                    "pattern",
                    "patterns",
                    # Physical elements
                    "rock",
                    "rocks",
                    "stone",
                    "stones"
                }
            },
            "forge_mastery": {
                "room": "torbrans_forge_hall",
                "verbs": {
                    # Forging actions
                    "forge",
                    "hammer",
                    "strike",
                    "shape",
                    "mold",
                    # Heat manipulation
                    "heat",
                    "quench",
                    "cool",
                    "temper",
                    "anneal",
                    # Crafting skills
                    "craft",
                    "create",
                    "design",
                    "etch",
                    "engrave"
                },
                "nouns": {
                    # Core materials
                    "metal",
                    "metals",
                    "ore",
                    "ores",
                    # Tools
                    "hammer",
                    "hammers",
                    "anvil",
                    "anvils",
                    # Forge elements
                    "flame",
                    "flames",
                    "forge",
                    "forges",
                    # Created items
                    "blade",
                    "blades",
                    "weapon",
                    "weapons",
                    # Magical elements
                    "rune",
                    "runes",
                    "sigil",
                    "sigils"
                }
            }
        }

    def _handle_completion(self) -> Tuple[bool, str]:
        """Check if all aspects are completed and handle completion."""
        if len(self._completed_groups) == len(self.aspects):
            self.completed = True
            if hasattr(self.game, 'game_state') and hasattr(self.game.game_state, 'progression'):
                self.game.game_state.progression.handle_puzzle_completion(
                    self.game.current_world.name, 
                    self.puzzle_id
                )
            return True, "The ground trembles with approval as the three earthen forces unite, carving a new path through the mountain!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "tophs_crystal_caverns",
            "rock_solid_chess_dojo",
            "torbrans_forge_hall"
        ])