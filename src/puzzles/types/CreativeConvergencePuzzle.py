from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
from puzzles.core.GenericPuzzleBase import GenericPuzzleBase

class CreativeConvergencePuzzle(GenericPuzzleBase):
    puzzle_type = "creative_convergence"
    
    def __init__(self):
        super().__init__(
            puzzle_id="creative_convergence_puzzle",
            name="Trial of Creative Mastery",
            description="Master the elements of creativity through artistic vision, surreal transformation, inventive brilliance, and master building",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "artistic_vision": {
                "room": "bob_ross_haven",
                "verbs": {
                    # Painting actions
                    "paint", "blend", "create", "stroke", "dab",
                    # Creative actions
                    "imagine", "envision", "dream", "compose", "craft",
                    # Nature manipulation
                    "shape", "grow", "form", "nurture", "plant"
                },
                "nouns": {
                    # Art tools
                    "brush", "brushes", "palette", "palettes",
                    # Nature elements
                    "tree", "trees", "cloud", "clouds",
                    # Art surfaces
                    "canvas", "canvases", "easel", "easels",
                    # Emotional elements
                    "joy", "joys", "friend", "friends",
                    # Studio elements
                    "studio", "studios", "light", "lights"
                }
            },
            "surreal_transformation": {
                "room": "cheshire_cats_grinning_abyss",
                "verbs": {
                    # Transformation actions
                    "fade", "morph", "shift", "warp", "twist",
                    # Expression actions
                    "grin", "laugh", "smile", "giggle", "smirk",
                    # Movement actions
                    "float", "swirl", "dance", "glide", "spiral"
                },
                "nouns": {
                    # Magical items
                    "potion", "potions", "bottle", "bottles",
                    # Abstract concepts
                    "reality", "realities", "dream", "dreams",
                    # Expressions
                    "smile", "smiles", "grin", "grins",
                    # Environment
                    "abyss", "abysses", "shadow", "shadows",
                    # Atmospheric elements
                    "mist", "mists", "void", "voids"
                }
            },
            "inventive_brilliance": {
                "room": "megaminds_misguided_mansion",
                "verbs": {
                    # Invention actions
                    "present", "invent", "design", "create", "build",
                    # Performance actions
                    "dramatize", "flourish", "pose", "gesture", "display",
                    # Scientific actions
                    "experiment", "analyze", "calculate", "measure", "test"
                },
                "nouns": {
                    # Clothing items
                    "cape", "capes", "collar", "collars",
                    # Inventions
                    "invention", "inventions", "device", "devices",
                    # Environment
                    "mansion", "mansions", "lair", "lairs",
                    # Characters
                    "minion", "minions", "genius", "geniuses",
                    # Scientific elements
                    "ray", "rays", "beam", "beams"
                }
            },
            "master_building": {
                "room": "utopian_lego_city",
                "verbs": {
                    # Building actions
                    "build", "construct", "assemble", "connect", "stack",
                    # Creative actions 
                    "design", "create", "craft", "make", "form",
                    # Instruction actions
                    "follow", "read", "study", "master", "learn"
                },
                "nouns": {
                    # Basic elements
                    "brick", "bricks", "block", "blocks",
                    # Building types
                    "tower", "towers", "building", "buildings",
                    # Instructions
                    "manual", "manuals", "guide", "guides",
                    # City elements
                    "city", "cities", "structure", "structures",
                    # Creation aspects
                    "model", "models", "design", "designs"
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
            return True, "The creative forces unite as painting, surrealism, invention, and master building combine, opening a whimsical path through imagination!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "bob_ross_haven",
            "cheshire_cats_grinning_abyss", 
            "megaminds_misguided_mansion",
            "utopian_lego_city"
        ])