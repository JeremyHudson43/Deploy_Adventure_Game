class BossBattle:
    def __init__(self, game):
        self.game = game
        self.choices = {
            "1": self._join_tezzeret,
            "2": self._fight_tezzeret, 
            "3": self._sabotage_portals
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
            "\nThe three fragments resonate together, opening a portal! You are pulled through...\n\n"
            "You find yourself in Tezzeret's final sanctum. The artificer stands before you, his etherium arm crackling with power.\n\n"
            "Tezzeret says: \n\nAt last. You've brought all three fragments. Finally, someone who understands true power."
        )
        
        self._show_choices()

    def _show_choices(self):
        """Display player choices."""
        self.game.display.print_message(
            "\nWhat do you do?\n\n"
            "1. Join Tezzeret and reshape reality\n\n"
            "2. Fight Tezzeret directly\n\n"
            "3. Sabotage the portal network"
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
            "\nTezzeret: YES! Finally, someone who understands! Together, we will forge a new multiverse!\n\n"
            "Reality warps around you as you and Tezzeret begin reshaping the very fabric of existence...\n\n"
            "ENDING: The Artificer's Apprentice"
        )
        self.game.quit()

    def _fight_tezzeret(self):
        """Handle fighting Tezzeret ending."""
        self.game.display.print_message(
            "\nTezzeret: Fool! You think mere artifacts can - wait, that energy signature... NO!\n\n"
            "The combined power of all three fragments overwhelms his defenses, reducing him to ash...\n\n"
            "ENDING: The Fragment Guardian"
        )
        self.game.quit()

    def _sabotage_portals(self):
        """Handle sabotaging portals ending."""
        self.game.display.print_message(
            "\nTezzeret: Yes... yes! The fragments are amplifying the portal field perfectly- wait, something's wrong...\n\n"
            "Your sabotage works perfectly as Tezzeret's form splinters across infinite realities...\n\n"
            "ENDING: The Portal Breaker"
        )
        self.game.quit()
