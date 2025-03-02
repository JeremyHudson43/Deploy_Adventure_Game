from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
from puzzles.core.GenericPuzzleBase import GenericPuzzleBase

class NostalgiaPuzzle(GenericPuzzleBase):
    puzzle_type = "nostalgia"
    
    def __init__(self):
        super().__init__(
            puzzle_id="nostalgia_puzzle",
            name="Trial of Childhood Memory",
            description="Master the elements of nostalgia through neighborly kindness, wonderland mischief, robotic innocence, and royal memories",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "neighborly_kindness": {
                "room": "mr_rogers_nostalgic_nexus",
                "verbs": {
                    # Helping actions
                    "share",
                    "help",
                    "teach",
                    "comfort",
                    "support",
                    # Friendly actions
                    "welcome",
                    "greet",
                    "smile",
                    "listen",
                    "care",
                    # Learning actions
                    "learn",
                    "explore",
                    "discover",
                    "imagine",
                    "create"
                },
                "nouns": {
                    # Clothing items
                    "cardigan",
                    "cardigans",
                    "shoe",
                    "shoes",
                    # Play items
                    "puppet",
                    "puppets",
                    "toy",
                    "toys",
                    # People
                    "neighbor",
                    "neighbors",
                    "friend",
                    "friends",
                    # Expressions
                    "smile",
                    "smiles",
                    "song",
                    "songs",
                    # Environment
                    "home",
                    "homes",
                    "room",
                    "rooms"
                }
            },
            "wonderland_mischief": {
                "room": "mad_hatters_temporal_trap",
                "verbs": {
                    # Tea party actions
                    "pour",
                    "stir",
                    "sip",
                    "serve",
                    "drink",
                    # Playful actions
                    "riddle",
                    "dance",
                    "laugh",
                    "play",
                    "sing",
                    # Time actions
                    "tick",
                    "tock",
                    "spin",
                    "whirl",
                    "twist"
                },
                "nouns": {
                    # Tea items
                    "tea",
                    "teas",
                    "cup",
                    "cups",
                    # Time pieces
                    "watch",
                    "watches",
                    "clock",
                    "clocks",
                    # Party elements
                    "party",
                    "parties",
                    "cake",
                    "cakes",
                    # Puzzle elements
                    "riddle",
                    "riddles",
                    "puzzle",
                    "puzzles",
                    # Time aspects
                    "time",
                    "times",
                    "moment",
                    "moments"
                }
            },
            "robotic_innocence": {
                "room": "walles_wonderful_world",
                "verbs": {
                    # Collection actions
                    "collect",
                    "gather",
                    "find",
                    "stack",
                    "sort",
                    # Care actions
                    "clean",
                    "tend",
                    "care",
                    "nurture",
                    "protect",
                    # Discovery actions
                    "discover",
                    "explore",
                    "examine",
                    "study",
                    "observe"
                },
                "nouns": {
                    # Nature elements
                    "plant",
                    "plants",
                    "boot",
                    "boots",
                    # Puzzle objects
                    "cube",
                    "cubes",
                    "puzzle",
                    "puzzles",
                    # Collection items
                    "treasure",
                    "treasures",
                    "trinket",
                    "trinkets",
                    # Environment
                    "world",
                    "worlds",
                    "tower",
                    "towers",
                    # Media
                    "tape",
                    "tapes",
                    "song",
                    "songs"
                }
            },
            "royal_nostalgia": {
                "room": "queen_of_hearts_grim_garden_party",
                "verbs": {
                    # Royal actions
                    "command",
                    "decree",
                    "rule",
                    "judge",
                    "proclaim",
                    # Garden actions
                    "plant",
                    "grow",
                    "tend",
                    "prune",
                    "paint",
                    # Party actions
                    "celebrate",
                    "feast",
                    "dance",
                    "play",
                    "sing"
                },
                "nouns": {
                    # Royal items
                    "crown",
                    "crowns",
                    "throne",
                    "thrones",
                    # Garden elements
                    "rose",
                    "roses",
                    "garden",
                    "gardens",
                    # Card elements
                    "heart",
                    "hearts",
                    "card",
                    "cards",
                    # Party elements
                    "tart",
                    "tarts",
                    "cake",
                    "cakes",
                    # Court elements
                    "court",
                    "courts",
                    "guard",
                    "guards"
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
            return True, "The nostalgic forces unite as kindness, mischief, innocence, and royalty combine, opening a heartwarming path through memory!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "mr_rogers_nostalgic_nexus",
            "mad_hatters_temporal_trap",
            "walles_wonderful_world",
            "queen_of_hearts_grim_garden_party"
        ])