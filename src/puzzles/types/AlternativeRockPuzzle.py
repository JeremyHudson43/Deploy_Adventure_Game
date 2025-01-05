from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
from puzzles.core.GenericPuzzleBase import GenericPuzzleBase

class AlternativeRockPuzzle(GenericPuzzleBase):
    puzzle_type = "alternative_rock"
    
    def __init__(self):
        super().__init__(
            puzzle_id="alternative_rock_puzzle",
            name="Trial of Rock Harmony",
            description="Master the elements of alternative rock through theatrical performance, emotional resonance, and energetic fusion",
            puzzle_type=self.puzzle_type
        )
        
        self._completed_groups = set()

        self.aspects = {
            "theatrical_performance": {
                "room": "panic_at_the_disco_boom_boom_ballroom",
                "verbs": {
                    # Performance actions
                    "dance",
                    "sing",
                    "perform",
                    "twirl",
                    "flourish",
                    # Theatrical moves
                    "bow",
                    "gesture",
                    "pose",
                    "strut",
                    "spin",
                    # Stage presence
                    "command",
                    "captivate",
                    "enchant",
                    "dazzle",
                    "entrance"
                },
                "nouns": {
                    # Stage elements
                    "stage",
                    "stages",
                    "spotlight",
                    "spotlights",
                    # Props
                    "hat",
                    "hats",
                    "glass",
                    "glasses",
                    # Venue features
                    "ballroom",
                    "ballrooms",
                    "curtain",
                    "curtains",
                    # Performance aspects
                    "dance",
                    "dances",
                    "song",
                    "songs",
                    # Atmosphere
                    "light",
                    "lights",
                    "glitter",
                    "glitters"
                }
            },
            "emotional_resonance": {
                "room": "twenty_one_pilots_trench_terminal",
                "verbs": {
                    # Expression actions
                    "feel",
                    "express",
                    "convey",
                    "reveal",
                    "share",
                    # Artistic actions
                    "paint",
                    "create",
                    "blend",
                    "craft",
                    "shape",
                    # Emotional states
                    "resonate",
                    "connect",
                    "understand",
                    "embrace",
                    "reflect"
                },
                "nouns": {
                    # Materials
                    "tape",
                    "tapes",
                    "paint",
                    "paints",
                    # Visual elements
                    "pattern",
                    "patterns",
                    "symbol",
                    "symbols",
                    # Emotional aspects
                    "emotion",
                    "emotions",
                    "feeling",
                    "feelings",
                    # Environment
                    "wall",
                    "walls",
                    "shadow",
                    "shadows",
                    # Underground elements
                    "trench",
                    "trenches",
                    "tunnel",
                    "tunnels"
                }
            },
            "energetic_fusion": {
                "room": "ajr_bang_boulevard",
                "verbs": {
                    # Musical actions
                    "play",
                    "blast",
                    "perform",
                    "create",
                    "mix",
                    # Movement actions
                    "jump",
                    "dance",
                    "bounce",
                    "spin",
                    "move",
                    # Celebration actions
                    "shout",
                    "celebrate",
                    "cheer",
                    "rejoice",
                    "party"
                },
                "nouns": {
                    # Instruments
                    "trumpet",
                    "trumpets",
                    "drum",
                    "drums",
                    # Performance elements
                    "confetti",
                    "confettis",
                    "note",
                    "notes",
                    # Environment
                    "street",
                    "streets",
                    "sign",
                    "signs",
                    # Light elements
                    "neon",
                    "neons",
                    "light",
                    "lights",
                    # Sound aspects
                    "beat",
                    "beats",
                    "sound",
                    "sounds"
                }
            },
            # Add the new aspect group to self.aspects:
            "visual_storytelling": {
                "room": "saint_motel_voyeur_vista",
                "verbs": {
                    # Camera actions
                    "record",
                    "capture",
                    "film",
                    "shoot",
                    "document",
                    # Vision actions
                    "observe",
                    "watch",
                    "witness",
                    "view",
                    "see",
                    # Story actions
                    "create",
                    "craft",
                    "weave",
                    "tell",
                    "share"
                },
                "nouns": {
                    # Film equipment
                    "film",
                    "films",
                    "reel",
                    "reels",
                    "camera",
                    "cameras",
                    # Visual elements
                    "scene",
                    "scenes",
                    "vista",
                    "vistas",
                    "moment",
                    "moments",
                    # Story elements
                    "story",
                    "stories",
                    "tale",
                    "tales",
                    # Atmosphere
                    "image",
                    "images",
                    "light",
                    "lights"
                }
            },
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
            return True, "The music swells in harmony as theatrics, emotion, and energy unite, opening a rhythmic path through the sound!"
        return False, ""

    def is_puzzle_room(self, room_id: str) -> bool:
        """Check if a room is part of this puzzle."""
        return any(location in room_id.lower() for location in [
            "panic_at_the_disco_boom_boom_ballroom",
            "twenty_one_pilots_trench_terminal",
            "ajr_bang_boulevard",
            "saint_motel_voyeur_vista"  # Add this line
        ])