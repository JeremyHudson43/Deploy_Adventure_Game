# src/command_system/inventory_processor.py

class InventoryManager:
    def __init__(self, player, display_manager):
        self.player = player
        self.display = display_manager

    def show_inventory(self):
        if not self.player.inventory:
            self.display.print_message("Your inventory is empty.")
        else:
            self.display.print_list("Your inventory", self.player.inventory, 
                              lambda item: f"{item}: {item.description}")

    def take(self, item_name: str):
        item = next((item for item in self.player.current_room.items 
                    if item.name.lower() == item_name.lower()), None)
        if item:
            self.player.inventory.add(item)
            self.player.current_room.items.remove(item)
            self.display.print_simple_message(f"You picked up the {item.name}.")
        else:
            self.display.print_simple_message(f"There's no '{item_name}' here to take.")

    def drop(self, item_name: str):
        item = next((item for item in self.player.inventory 
                    if item.name.lower() == item_name.lower()), None)
        if item:
            self.player.inventory.remove(item)
            self.player.current_room.items.add(item)
            self.display.print_simple_message(f"You drop the {item.name}.")
        else:
            self.display.print_simple_message(f"You don't have a '{item_name}' to drop.")

    def use(self, item_name: str):
        item = next((item for item in self.player.inventory 
                    if item.name.lower() == item_name.lower()), None)
        if item:
            # Add specific item use logic here
            self.display.print_simple_message(f"You use the {item.name}.")
        else:
            self.display.print_simple_message(f"You don't have a '{item_name}' to use.")
