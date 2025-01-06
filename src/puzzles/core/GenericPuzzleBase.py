from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
import random

class GenericPuzzleBase(BasePuzzle):
    """Base class for all puzzles that use the verb/noun command structure"""
    
    # Theme-specific messages based on room keywords
    THEMED_MESSAGES = {
        # Default
        "default": {
            "verb": ["That action might work... but you need something to use it on."],
            "noun": ["That's something you could use... but you need the right action."]
        }
    }

    def _get_themed_messages(self, room_id: str) -> Dict:
        """Get appropriate themed messages based on room name"""
        room_id = room_id.lower()
        for theme in self.THEMED_MESSAGES:
            if theme in room_id:
                return self.THEMED_MESSAGES[theme]
        return self.THEMED_MESSAGES["default"]

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