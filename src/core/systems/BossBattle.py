class BossBattle:
    def __init__(self, game):
        self.game = game
        self.choices = {
            "1": self._join_tezzeret,
            "2": self._fight_tezzeret,
            "3": self._pile_drive_tezzeret
        }

    def check_fragments(self):
        """Check if player has all three fragments."""
        fragments = ["elemental shard", "resonance shard", "imagination shard"]
        inventory_names = [item.name.lower() for item in self.game.player.inventory]
        return all(f in inventory_names for f in fragments)

    def trigger_battle(self):
        """Start the boss battle sequence."""
        if not self.check_fragments():
            return

        self.game.display.print_message(
            "\nThe three fragments resonate together, unlocking ancient energies within you. A surge of overwhelming power courses through your veins...\n\n"
            "You find yourself face to face with Tezzeret, the master artificer, his etherium arm sparking with raw, untamed energy.\n\n"
            "Tezzeret says:\n\n"
            "'At last. You've brought the fragments to me. Do you truly grasp the potential of what you hold? Or are you just another fool blinded by power?'"
        )

        self._show_choices()

    def _show_choices(self):
        """Display player choices."""
        self.game.display.print_message(
            "\nWhat do you do? Enter a number\n\n"
            "1. Join Tezzeret and reshape reality\n\n"
            "2. Fight Tezzeret directly\n\n"
            "3. ???"
        )

        choice = input("Enter your choice (1-3): \n").strip()

        if choice in self.choices:
            self.choices[choice]()
        else:
            print("\n\nInvalid choice. The fragments pulse warningly...")
            self._show_choices()

    def _join_tezzeret(self):
        """Handle joining Tezzeret ending."""
        self.game.display.print_message(
            "\nTezzeret's eyes gleam with triumph as you extend your hand in agreement.\n\n"
            "'YES!' he bellows. 'Together, we shall tear down the flawed multiverse and rebuild it in perfection!'\n\n"
            "Etherium spreads from his arm to yours, merging your very essence with his boundless ingenuity. The shards amplify your combined intellect, granting the power to reshape the cosmos.\n\n"
            "Over countless eons, you and Tezzeret weave a new reality, bending creation to your will.\n\n"
            "ENDING: The Artificer's Ascension"
        )
        self.game.quit()

    def _fight_tezzeret(self):
        """Handle fighting Tezzeret ending."""
        self.game.display.print_message(
            "\nTezzeret snarls, his etherium arm flaring as he summons a storm of arcane machinery to crush you.\n\n"
            "But the shards in your possession glow with an ancient energy, combining their forces into an unstoppable wave of power.\n\n"
            "Tezzeret screams as the energy tears through him. His form shatters into countless fragments, each piece flung to the furthest reaches of the multiverse.\n\n"
            "All that remains is silence as the shards' glow fades, leaving behind a world finally free of his tyranny.\n\n"
            "ENDING: The Fractured Architect"
        )
        self.game.quit()

    def _pile_drive_tezzeret(self):
        """Handle ??? pile-driving Tezzeret ending."""
        self.game.display.print_message(
            "\nTezzeret: 'You dare challenge me? You're nothing but—wait, what are you doing?!'\n\n"
            "Ignoring his etherium-enhanced threats, you leap into the air, spinning with a grace that defies physics. With impossible strength, you seize Tezzeret mid-monologue.\n\n"
            "A spinning pile driver of such sheer force slams him into the ground that his neck snaps with a sickening crack. His body lies motionless, the once-mighty artificer defeated in the most absurdly humiliating way imaginable.\n\n"
            "'How...?' is all he manages to croak as you stand victorious over his crumpled form.\n\n"
            "ENDING: The Spinning Titan"
        )
        self.game.quit()
