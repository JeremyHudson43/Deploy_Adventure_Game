from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
import random

class GenericPuzzleBase(BasePuzzle):
    """Base class for all puzzles that use the verb/noun command structure"""
    
    # Theme-specific messages based on room keywords
    THEMED_MESSAGES = {
        # ELEMENTAL CONFLUX
        "level_one": {  # Air level
            "verb": "That's a known airbending technique... but you need something to use it on.",
            "noun": "That's something you could airbend... but you need the right technique."
        },
        "level_two": {  # Earth level
            "verb": "That's a way to manipulate earth... but you need something to target.",
            "noun": "That's something you could manipulate... but you need an earthbending technique."
        },
        "level_three": {  # Fire level
            "verb": "That's a firebending move... but you need something to direct it at.",
            "noun": "That's something you could bend fire with... but you need the right technique."
        },
        "level_four": {  # Water level
            "verb": "That's a waterbending form... but you need something to flow through.",
            "noun": "That's something you could bend water around... but you need the right form."
        },
        "level_five": {  # Spirit level
            "verb": "That's a spiritual technique... but you need something to focus it on.",
            "noun": "That's something with spiritual energy... but you need the right technique."
        },

        # HARMONIC NEXUS
        "level_one": {  # Alternative Rock level
            "verb": "That's a proper performance move... but what will you perform with?",
            "noun": "That's something you could perform with... but you need the right move."
        },
        "level_two": {  # 8-bit level
            "verb": "That's a good pixel manipulation... but what will you render?",
            "noun": "Those are some nice sprites... but you need the right manipulation."
        },
        "level_three": {  # Steampunk level
            "verb": "That's a proper mechanical action... but what will you adjust?",
            "noun": "That's a suitable mechanism... but you need the right action."
        },

        # WHIMSICAL REALM
        "level_one": {  # Creative level (Bob Ross, Megamind, etc)
            "verb": "That's a creative technique... but what will you make?",
            "noun": "That's something worth creating with... but you need the right technique."
        },
        "level_two": {  # Wonderland level (Mad Hatter, Queen, etc)
            "verb": "That's properly mad... but what will you do it to?",
            "noun": "That's curiously perfect... but needs a properly mad action."
        },
        "level_three": {  # Childhood level (Toaster, Blanka, etc)
            "verb": "That's a playful action... but what will you play with?",
            "noun": "That's something fun to play with... but you need the right action."
        },

        # Default
        "default": {
            "verb": "That action might work... but you need something to use it on.",
            "noun": "That's something you could use... but you need the right action."
        }
    }

    def _get_themed_messages(self, room_id: str) -> Dict:
        """Get appropriate themed messages based on room's level"""
        room_id = room_id.lower()
        
        # Extract level from room_id (format is typically "level_one/room_name")
        level = "default"
        if "/" in room_id:
            level = room_id.split("/")[0]
            
        return self.THEMED_MESSAGES.get(level, self.THEMED_MESSAGES["default"])

    def _get_success_message(self, aspect: str) -> str:
        """Get success message for completing an aspect. Can be overridden by child classes."""
        # Convert aspect from snake_case to readable form
        aspect_name = aspect.replace('_', ' ')
        return f"The {aspect_name} grows stronger!"

    def handle_command(self, command: str, room_id: str, inventory: List[str]) -> Tuple[bool, str]:
        """Generic command handler for verb/noun puzzles"""
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
                verb_correct = verb in data["verbs"]
                noun_correct = noun in data["nouns"]
                themed_messages = self._get_themed_messages(room_id)

                if verb_correct and noun_correct:
                    self._completed_groups.add(aspect)
                    completed, msg = self._handle_completion()
                    if completed:
                        return True, msg
                    return True, self._get_success_message(aspect)
                
                elif verb_correct:
                    return False, random.choice(themed_messages["verb"])
                
                elif noun_correct:
                    return False, random.choice(themed_messages["noun"])

        return False, "Nothing happens."