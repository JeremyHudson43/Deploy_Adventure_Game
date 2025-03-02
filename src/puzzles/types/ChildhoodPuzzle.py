from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
from puzzles.core.GenericPuzzleBase import GenericPuzzleBase

class ChildhoodPuzzle(GenericPuzzleBase):
    puzzle_type = "childhood"
    
    def __init__(self):
        super().__init__(
            puzzle_id="childhood_puzzle",
            name="Trial of Wonder",
            description="Master the elements of childhood through appliance friendship, electric adventure, infinite snacks, and eternal triumph",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "appliance_friendship": {
                "room": "the_brave_little_toasters_appliance_uprising",
                "verbs": {
                    # Unity actions
                    "unite",
                    "gather",
                    "join",
                    "band",
                    "assemble",
                    # Leadership actions
                    "rally",
                    "lead",
                    "guide",
                    "direct",
                    "inspire",
                    # Support actions
                    "support",
                    "help",
                    "comfort",
                    "encourage",
                    "protect"
                },
                "nouns": {
                    # Appliances
                    "toaster",
                    "toasters",
                    "lamp",
                    "lamps",
                    # Relationships
                    "friend",
                    "friends",
                    "ally",
                    "allies",
                    # Emotional aspects
                    "spirit",
                    "spirits",
                    "heart",
                    "hearts",
                    # Character traits
                    "courage",
                    "courages",
                    "dream",
                    "dreams",
                    # Group terms
                    "team",
                    "teams",
                    "family",
                    "families"
                }
            },
            "electric_adventure": {
                "room": "blankas_electrifying_jungle",
                "verbs": {
                    # Energy actions
                    "spark",
                    "flash",
                    "crackle",
                    "surge",
                    "zap",
                    # Movement actions
                    "jump",
                    "roll",
                    "flip",
                    "spin",
                    "dash",
                    # Combat moves
                    "attack",
                    "charge",
                    "strike",
                    "blast",
                    "shock"
                },
                "nouns": {
                    # Energy forms
                    "lightning",
                    "lightnings",
                    "thunder",
                    "thunders",
                    # Environment
                    "jungle",
                    "jungles",
                    "tree",
                    "trees",
                    # Power elements
                    "energy",
                    "energies",
                    "power",
                    "powers",
                    # Battle aspects
                    "move",
                    "moves",
                    "skill",
                    "skills",
                    # Weather elements
                    "storm",
                    "storms",
                    "cloud",
                    "clouds"
                }
            },
            "infinite_snacks": {
                "room": "sheetz_station_of_infinite_delight",
                "verbs": {
                    # Food actions
                    "taste",
                    "sip",
                    "drink",
                    "nibble",
                    "munch",
                    # Creation actions
                    "mix",
                    "blend",
                    "create",
                    "craft",
                    "prepare",
                    # Experience actions
                    "enjoy",
                    "savor",
                    "delight",
                    "relish",
                    "indulge"
                },
                "nouns": {
                    # Beverages
                    "slushie",
                    "slushies",
                    "drink",
                    "drinks",
                    # Food items
                    "snack",
                    "snacks",
                    "treat",
                    "treats",
                    # Store elements
                    "shelf",
                    "shelves",
                    "aisle",
                    "aisles",
                    # Magic aspects
                    "magic",
                    "magics",
                    "wonder",
                    "wonders",
                    # Joy aspects
                    "delight",
                    "delights",
                    "joy",
                    "joys"
                }
            },
            "eternal_triumph": {
                "room": "pickleball_court_of_eternal_triumph",
                "verbs": {
                    # Victory actions
                    "win",
                    "triumph",
                    "conquer",
                    "achieve",
                    "master",
                    # Play actions
                    "serve",
                    "volley",
                    "smash",
                    "dink",
                    "rally",
                    # Spirit actions
                    "celebrate",
                    "cheer",
                    "laugh",
                    "smile",
                    "dance"
                },
                "nouns": {
                    # Equipment
                    "paddle",
                    "paddles",
                    "ball",
                    "balls",
                    # Court elements
                    "court",
                    "courts",
                    "line",
                    "lines",
                    # Victory elements
                    "victory",
                    "victories",
                    "trophy",
                    "trophies",
                    # Spirit elements
                    "spirit",
                    "spirits",
                    "joy",
                    "joys",
                    # Team elements
                    "team",
                    "teams",
                    "partner",
                    "partners"
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
            return True, "The childhood dreams unite as friendship, adventure, delight, and triumph combine, opening a magical path through wonder!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "the_brave_little_toasters_appliance_uprising",
            "blankas_electrifying_jungle",
            "sheetz_station_of_infinite_delight",
            "pickleball_court_of_eternal_triumph"
        ])