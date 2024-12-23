class BossBattle:
    def __init__(self, game):
        self.game = game
        self.choices = {
            "1": self._join_tezzeret,
            "2": self._fight_tezzeret, 
            "3": self._sabotage_portals
        }

    def check_fragments(self):
        """Check if player has all three fragments"""
        fragments = [
            "spirit_crystal_fragment",
            "resonance_core_fragment", 
            "imagination_shard_fragment"
        ]
        
        inventory_names = [item.name.lower() for item in self.game.player.inventory]
        return all(f in inventory_names for f in fragments)

    def trigger_battle(self):
        """Start the boss battle sequence"""
        if not self.check_fragments():
            return
            
        self.game.display.print_message("\nThe three fragments resonate together, opening a portal! You are pulled through...")
        self.game.display.print_message("\nYou find yourself in Tezzeret's final sanctum. The artificer stands before you, his etherium arm crackling with power.")
        self.game.display.print_message("\nTezzeret: At last. You've brought all three fragments. Finally, someone who understands true power.")
        
        self._show_choices()

    def _show_choices(self):
        """Display player choices"""
        self.game.display.print_message("\nWhat do you do?")
        self.game.display.print_message("\n1. Join Tezzeret and reshape reality")
        self.game.display.print_message("2. Fight Tezzeret directly")
        self.game.display.print_message("3. Sabotage the portal network")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice in self.choices:
            self.choices[choice]()
        else:
            self.game.display.print_message("\nInvalid choice. The fragments pulse warningly...")
            self._show_choices()

    def _join_tezzeret(self):
        """Handle joining Tezzeret ending"""
        self.game.display.print_message("\nTezzeret: YES! Finally, someone who understands! Together, we will forge a new multiverse!")
        self.game.display.print_message("\nReality warps around you as you and Tezzeret begin reshaping the very fabric of existence...")
        self.game.display.print_message("\nENDING: The Artificer's Apprentice")
        self.game.quit()

    def _fight_tezzeret(self):
        """Handle fighting Tezzeret ending"""
        self.game.display.print_message("\nTezzeret: Fool! You think mere artifacts can - wait, that energy signature... NO!")
        self.game.display.print_message("\nThe combined power of all three fragments overwhelms his defenses, reducing him to ash...")
        self.game.display.print_message("\nENDING: The Fragment Guardian")
        self.game.quit()

    def _sabotage_portals(self):
        """Handle sabotaging portals ending"""
        self.game.display.print_message("\nTezzeret: Yes... yes! The fragments are amplifying the portal field perfectly- wait, something's wrong...")
        self.game.display.print_message("\nYour sabotage works perfectly as Tezzeret's form splinters across infinite realities...")
        self.game.display.print_message("\nENDING: The Portal Breaker")
        self.game.quit()