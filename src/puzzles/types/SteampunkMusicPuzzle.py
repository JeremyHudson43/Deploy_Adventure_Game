from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
from puzzles.core.GenericPuzzleBase import GenericPuzzleBase

class SteampunkMusicPuzzle(GenericPuzzleBase):
    puzzle_type = "steampunk_music"
    
    def __init__(self):
        super().__init__(
            puzzle_id="steampunk_music_puzzle",
            name="Trial of Clockwork Harmony",
            description="Master the elements of steampunk through mechanical performance, temporal resonance, and aerial orchestration",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "mechanical_performance": {
                "room": "steam_powered_giraffes_clockwork_stage",
                "verbs": {
                    # Mechanical actions
                    "sync",
                    "wind",
                    "turn",
                    "align",
                    "calibrate",
                    # Performance actions
                    "perform",
                    "dance",
                    "sing",
                    "move",
                    "gesture",
                    # Engineering actions
                    "adjust",
                    "tune",
                    "maintain",
                    "regulate",
                    "operate"
                },
                "nouns": {
                    # Mechanical parts
                    "gear",
                    "gears",
                    "valve",
                    "valves",
                    # Power sources
                    "steam",
                    "steams",
                    "boiler",
                    "boilers",
                    # Performance elements
                    "stage",
                    "stages",
                    "automaton",
                    "automatons",
                    # Musical components
                    "brass",
                    "brasses",
                    "pipe",
                    "pipes",
                    # Machine parts
                    "spring",
                    "springs",
                    "lever",
                    "levers"
                }
            },
            "temporal_resonance": {
                "room": "the_cog_is_deads_temporal_laboratory",
                "verbs": {
                    # Time manipulation
                    "reverse",
                    "flow",
                    "bend",
                    "warp",
                    "shift",
                    # Mechanical actions
                    "tick",
                    "turn",
                    "spin",
                    "rotate",
                    "oscillate",
                    # Scientific actions
                    "experiment",
                    "observe",
                    "measure",
                    "analyze",
                    "calculate"
                },
                "nouns": {
                    # Time devices
                    "clock",
                    "clocks",
                    "chronometer",
                    "chronometers",
                    # Time aspects
                    "time",
                    "times",
                    "moment",
                    "moments",
                    # Musical elements
                    "rhythm",
                    "rhythms",
                    "note",
                    "notes",
                    # Scientific equipment
                    "device",
                    "devices",
                    "instrument",
                    "instruments",
                    # Laboratory elements
                    "experiment",
                    "experiments",
                    "mechanism",
                    "mechanisms"
                }
            },
            "aerial_orchestration": {
                "room": "abney_parks_steampunk_airship",
                "verbs": {
                    # Navigation
                    "sail",
                    "navigate",
                    "steer",
                    "pilot",
                    "guide",
                    # Music direction
                    "conduct",
                    "direct",
                    "orchestrate",
                    "harmonize",
                    "compose",
                    # Aerial actions
                    "soar",
                    "glide",
                    "float",
                    "drift",
                    "hover"
                },
                "nouns": {
                    # Ship parts
                    "deck",
                    "decks",
                    "sail",
                    "sails",
                    # Navigation tools
                    "compass",
                    "compasses",
                    "chart",
                    "charts",
                    # Musical equipment
                    "instrument",
                    "instruments",
                    "horn",
                    "horns",
                    # Weather elements
                    "wind",
                    "winds",
                    "cloud",
                    "clouds",
                    # Ship elements
                    "hull",
                    "hulls",
                    "propeller",
                    "propellers"
                }
            }
        }

    def _check_overall_completion(self) -> Tuple[bool, str]:
        """If all aspects are done, mark the puzzle as complete and return a final message."""
        if len(self._completed_groups) == len(self.aspects):
            self.completed = True
            return True, (
                "The clockwork mechanisms align as mechanics, time, and wind unite. "
                "A steam-powered path opens through the gears!"
            )
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "steam_powered_giraffes_clockwork_stage",
            "the_cog_is_deads_temporal_laboratory",
            "abney_parks_steampunk_airship"
        ])