from typing import Dict, List, Tuple, Optional
from puzzles.core.BasePuzzle import BasePuzzle
import random

class GenericPuzzleBase(BasePuzzle):
    """Base class for all puzzles that use the verb/noun command structure"""
    
    # Theme-specific messages based on room keywords
    THEMED_MESSAGES = {
        # Air/Wind themes
        "airbending": {
            "verb": [
                "The winds stir at your command... but seek a proper focus.",
                "Air responds to your motion... but needs direction.",
                "Your technique disturbs the breeze... though it wants a target.",
                "The currents acknowledge your gesture... but require purpose.",
                "You shape the air with skill... yet it yearns for more."
            ],
            "noun": [
                "The air swirls around this... awaiting the proper technique.",
                "Breezes gather here... but need guidance.",
                "The winds recognize this... though your approach is wrong.",
                "Air currents dance about this focus... but how to direct them?",
                "This draws the attention of the breeze... but requires mastery."
            ]
        },
        # Storm/Thunder themes
        "storm": {
            "verb": [
                "Thunder acknowledges your action... but lacks focus.",
                "Lightning crackles at your command... yet seeks a target.",
                "The storm responds to your call... though incompletely.",
                "Your gesture carries electric potential... but needs direction.",
                "The tempest recognizes your method... awaiting its purpose."
            ],
            "noun": [
                "Storm energies gather here... but need proper direction.",
                "Lightning dances around this... seeking proper guidance.",
                "Thunder rumbles in recognition... but your approach is wrong.",
                "The tempest stirs at this... though requires different action.",
                "This calls to the storm... but demands proper technique."
            ]
        },
        # Fire/Flame themes
        "flame": {
            "verb": [
                "The flames flicker at your command... but lack focus.",
                "Fire responds to your gesture... yet seeks its target.",
                "Embers dance at your action... though need direction.",
                "Your technique carries heat... but requires purpose.",
                "The fire acknowledges your way... awaiting proper focus."
            ],
            "noun": [
                "Heat gathers around this... but needs proper guidance.",
                "The flames dance about this... seeking true command.",
                "Fire stirs in recognition... though your approach falters.",
                "This resonates with burning potential... but requires mastery.",
                "The embers acknowledge this... yet await proper action."
            ]
        },
        # Water/Ocean themes
        "water": {
            "verb": [
                "The waters stir at your command... but seek direction.",
                "Waves respond to your motion... yet need focus.",
                "Your technique ripples outward... though incompletely.",
                "The currents acknowledge your gesture... but want purpose.",
                "You shape the waters with promise... awaiting true focus."
            ],
            "noun": [
                "The waters gather here... but need proper guidance.",
                "Waves circle around this... seeking true command.",
                "The currents recognize this... though your approach wavers.",
                "This draws the tide's attention... but requires mastery.",
                "Water dances about this focus... yet awaits proper action."
            ]
        },
        # Music/Sound themes
        "music": {
            "verb": [
                "The melody stirs at your action... but seeks harmony.",
                "Rhythms respond to your gesture... yet need focus.",
                "Your technique carries a tune... though incomplete.",
                "The music acknowledges your way... but wants direction.",
                "You shape the song with promise... awaiting true purpose."
            ],
            "noun": [
                "Harmonies gather here... but need proper guidance.",
                "The melody circles this... seeking true command.",
                "Music stirs in recognition... though your approach falters.",
                "This resonates with potential... but requires mastery.",
                "Notes dance about this focus... yet await proper action."
            ]
        },
        # Spirit/Ethereal themes
        "spirit": {
            "verb": [
                "Ethereal energies acknowledge your action... but seek focus.",
                "The spirits stir at your command... yet need direction.",
                "Your technique touches the veil... though incompletely.",
                "Mystic forces respond to your gesture... but want purpose.",
                "You shape ethereal powers with promise... awaiting true focus."
            ],
            "noun": [
                "Spiritual energy gathers here... but needs proper guidance.",
                "The veil thins around this... seeking true command.",
                "Mystic forces recognize this... though your approach wavers.",
                "This draws ethereal attention... but requires mastery.",
                "Spirit energies circle this focus... yet await proper action."
            ]
        },
        # Default messages if no theme matches
        "default": {
            "verb": [
                "Your action holds power... but its target eludes you.",
                "The way you move shows promise... but towards what?",
                "There's wisdom in that action... but it seeks something more.",
                "Your approach resonates... but lacks proper focus.",
                "That method pulses with potential... but needs direction."
            ],
            "noun": [
                "Something stirs in response... but requires the right approach.",
                "You sense importance here... yet the means escape you.",
                "This draws your attention... but demands different action.",
                "You're drawn to this... though your approach isn't quite right.",
                "There's meaning to be found here... but not like that."
            ]
        },# [Previous themes remain the same, adding new ones:]

        # Bob Ross/Painting themes
        "ross": {
            "verb": [
                "Your artistic technique has potential... but needs a happier subject.",
                "That's a happy little action... seeking its canvas.",
                "Your creative gesture flows... but hasn't found its joy.",
                "The brush moves with promise... though needs its muse.",
                "You paint with spirit... but what will you create?"
            ],
            "noun": [
                "A delightful subject... awaiting your artistic touch.",
                "What a happy little thing... but how will you capture it?",
                "This could be our little secret... if you knew how to paint it.",
                "Nature's beauty calls here... but needs the right strokes.",
                "Such wonderful inspiration... though your technique needs joy."
            ]
        },
        # Megamind/Presentation themes
        "megamind": {
            "verb": [
                "PRESENTATION! Good technique... but what's your target?",
                "Delightfully evil action... though needs proper focus.",
                "Wonderfully dramatic gesture... but lacks a subject.",
                "Now that's a super villain move... seeking its moment.",
                "Your flair is showing... but where will you direct it?"
            ],
            "noun": [
                "Oh, you're a villain alright... but how will you present this?",
                "Now THAT'S an evil plan... awaiting proper execution.",
                "Ollo! This has potential... but needs more drama.",
                "This could be delightfully evil... with the right presentation.",
                "A proper villain's tool... though your technique lacks PRESENTATION!"
            ]
        },
        # Alice in Wonderland/Mad themes
        "hatter": {
            "verb": [
                "A perfectly mad approach... but to what, I wonder?",
                "Time approves of that action... though needs its tea party.",
                "Quite the wonderland gesture... seeking its madness.",
                "How curiouser and curiouser... but what's your target?",
                "Mad as a hatter, that move... though needs direction."
            ],
            "noun": [
                "Well that's properly mad... but how will you use it?",
                "Worthy of an unbirthday... if you knew what to do.",
                "The madness recognizes this... awaiting proper teatime.",
                "Time himself would approve... if your technique matched.",
                "Something wonderlandish here... but needs madder methods."
            ]
        },
        # Chiptune/8-bit themes
        "bit": {
            "verb": [
                "Your input sequence shows promise... but needs proper data.",
                "That code execution flows... seeking its variable.",
                "Program function recognized... though lacks parameters.",
                "Runtime looks good... but requires target address.",
                "Pixel-perfect action... awaiting data structure."
            ],
            "noun": [
                "Data structure detected... but needs proper algorithms.",
                "Valid variable found... seeking execution method.",
                "Memory address recognized... though requires proper input.",
                "Sprite data located... but needs animation sequence.",
                "Bitmap identified... awaiting proper rendering."
            ]
        },
        # Steampunk themes
        "clockwork": {
            "verb": [
                "Gears whir at your command... but seek their mechanism.",
                "Steam pressure builds promisingly... though needs its valves.",
                "The brass responds to your touch... but requires calibration.",
                "Mechanical precision noted... seeking proper apparatus.",
                "Your technique has proper torque... awaiting its machinery."
            ],
            "noun": [
                "The mechanisms acknowledge this... but need proper operation.",
                "Brass and copper resonate here... seeking the right adjustment.",
                "Steam gathers about this focus... though requires proper pressure.",
                "Gears align with this purpose... but need precise calibration.",
                "The machinery recognizes this... awaiting proper technique."
            ]
        },
        # Alternative Rock themes
        "trench": {
            "verb": [
                "The underground stirs at your signal... but seeks its echo.",
                "Your technique carries the rhythm... though needs its voice.",
                "The shadows dance to your movement... seeking resonance.",
                "Yellow tape marks your path... but where does it lead?",
                "The city hears your call... awaiting proper harmony."
            ],
            "noun": [
                "The underground recognizes this... but needs its signal.",
                "Echoes gather here... seeking proper amplification.",
                "The city's pulse aligns with this... though needs direction.",
                "Shadows mark this significance... but require proper movement.",
                "The rhythm acknowledges this... awaiting your signal."
            ]
        }
    }

    def _get_themed_messages(self, room_id: str) -> Dict:
        """Get appropriate themed messages based on room name"""
        room_id = room_id.lower()
        for theme in self.THEMED_MESSAGES:
            if theme in room_id:
                return self.THEMED_MESSAGES[theme]
        return self.THEMED_MESSAGES["default"]

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