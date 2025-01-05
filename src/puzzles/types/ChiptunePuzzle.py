from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
from puzzles.core.GenericPuzzleBase import GenericPuzzleBase

class ChiptunePuzzle(GenericPuzzleBase):
    puzzle_type = "chiptune"
    
    def __init__(self):
        super().__init__(
            puzzle_id="chiptune_puzzle",
            name="Trial of Digital Harmony",
            description="Master the elements of chiptune through epic composition, retro fusion, and kawaii beats",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "epic_composition": {
                "room": "darren_korb_supergiant_studio",
                "verbs": {
                    # Music creation
                    "compose",
                    "arrange",
                    "orchestrate",
                    "conduct",
                    "write",
                    # Performance
                    "strum",
                    "play",
                    "perform",
                    "record",
                    "create",
                    # Sound mixing
                    "layer",
                    "blend",
                    "mix",
                    "balance",
                    "harmonize"
                },
                "nouns": {
                    # Instruments
                    "guitar",
                    "guitars",
                    "string",
                    "strings",
                    # Musical elements
                    "melody",
                    "melodies",
                    "rhythm",
                    "rhythms",
                    # Equipment
                    "shield",
                    "shields",
                    "amplifier",
                    "amplifiers",
                    # Sound aspects
                    "note",
                    "notes",
                    "chord",
                    "chords",
                    # Studio elements
                    "track",
                    "tracks",
                    "studio",
                    "studios"
                }
            },
            "retro_fusion": {
                "room": "qumu_8_bit_oasis",
                "verbs": {
                    # Sound manipulation
                    "remix",
                    "sync",
                    "tune",
                    "program",
                    "code",
                    # Digital creation
                    "generate",
                    "process",
                    "sequence",
                    "modulate",
                    "synthesize",
                    # Artistic actions
                    "draw",
                    "paint",
                    "design",
                    "create",
                    "render"
                },
                "nouns": {
                    # Digital tools
                    "synth",
                    "synths",
                    "pixel",
                    "pixels",
                    # Sound elements
                    "beat",
                    "beats",
                    "wave",
                    "waves",
                    # Technical terms
                    "chip",
                    "chips",
                    "bit",
                    "bits",
                    # Visual elements
                    "screen",
                    "screens",
                    "sprite",
                    "sprites",
                    # Environment
                    "oasis",
                    "oases",
                    "paradise",
                    "paradises"
                }
            },
            "kawaii_beats": {
                "room": "snails_house_beep_boop_arcade",
                "verbs": {
                    # Playful actions
                    "play",
                    "bounce",
                    "dance",
                    "jump",
                    "skip",
                    # Sound effects
                    "beep",
                    "boop",
                    "chirp",
                    "ping",
                    "chime",
                    # Game actions
                    "score",
                    "win",
                    "level",
                    "achieve",
                    "unlock"
                },
                "nouns": {
                    # Cute elements
                    "heart",
                    "hearts",
                    "plush",
                    "plushies",
                    # Game items
                    "token",
                    "tokens",
                    "coin",
                    "coins",
                    # Digital aspects
                    "sprite",
                    "sprites",
                    "pixel",
                    "pixels",
                    # Arcade elements
                    "game",
                    "games",
                    "cabinet",
                    "cabinets",
                    # Sound elements
                    "tune",
                    "tunes",
                    "melody",
                    "melodies"
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
            return True, "The digital sounds harmonize as epic, retro, and kawaii unite, opening a pixelated path through the code!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "darren_korb_supergiant_studio",
            "qumu_8_bit_oasis",
            "snails_house_beep_boop_arcade"
        ])