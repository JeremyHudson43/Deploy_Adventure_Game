class MovementManager:
    def __init__(self, player, display_manager, game):
        self.player = player
        self.display = display_manager
        self.game = game

    def go(self, direction: str):
        """Handle normal directional movement."""
        current_room = self.player.current_room
        if direction in current_room.exits():
            target_room = getattr(current_room, direction)
            if target_room:
                # Get the target room ID
                if isinstance(target_room, str):
                    target_room_id = target_room
                else:
                    # If it's a Room object, get its ID from the world's rooms
                    target_room_id = None
                    for room_id, room in self.game.current_world.rooms.items():
                        if room == target_room:
                            target_room_id = room_id
                            break
                    if target_room_id is None:
                        target_room_id = target_room.name  # Fallback to name if not found

                # Check if the room is locked using progression system
                if self.game.current_world and hasattr(self.game.current_world, 'progression'):
                    if not self.game.current_world.progression.is_room_accessible(
                        self.game.current_world.name, target_room_id
                    ):
                        self.display.print_message("This area is locked. Complete the current level's challenges to proceed.")
                        return

                # Get the room using the world's normalization
                target_room = self.game.current_world.get_room(target_room_id)
                if target_room:
                    self.player.move_to(target_room)
                    self.game.command_processor.look()
                else:
                    self.display.print_message(f"Error: Room '{target_room_id}' not found.")
            else:
                self.display.print_message(f"Cannot go {direction} from here.")
        else:
            self.display.print_message(f"There is no exit {direction} from here.")

    def use_stairs(self, direction: str):
        """Handle vertical movement using stairs."""
        current_room = self.player.current_room
        new_room_id = None

        if direction == "up":
            if hasattr(current_room, 'stairs_up') and current_room.stairs_up:
                new_room_id = current_room.stairs_up
            else:
                self.display.print_message("There are no stairs going up here.")
                return

        elif direction == "down":
            if hasattr(current_room, 'stairs_down') and current_room.stairs_down:
                new_room_id = current_room.stairs_down
            else:
                self.display.print_message("There are no stairs going down here.")
                return

        if new_room_id:
            # Check if the room is locked using progression system
            if self.game.current_world and hasattr(self.game.current_world, 'progression'):
                if not self.game.current_world.progression.is_room_accessible(
                    self.game.current_world.name, new_room_id
                ):
                    self.display.print_message("This area is locked. Complete the current level's challenges to proceed.")
                    return

            new_room = self.game.current_world.get_room(new_room_id)
            if new_room:
                self.player.move_to(new_room)
                self.game.command_processor.look()
            else:
                self.display.print_message(f"Error: Room '{new_room_id}' not found.")

    def teleport(self, world_name):
        """Handle teleporting between worlds."""
        if not world_name:
            return "Please specify a world to teleport to."
        
        target_world = world_name.lower().replace(" ", "")
        available_worlds = self.game.worlds
        
        for name, world in available_worlds.items():
            if name.lower().replace(" ", "") == target_world:
                self.game.current_world = world
                starting_room = world.get_starting_room()
                self.player.move_to(starting_room)
                self.display.print_message(f"You have teleported to {name}.")
                # Add the new help prompt
                self.display.print_message("Type 'help' to see world-specific commands and available actions.")
                self.game.command_processor.look()
                return
        
        self.display.print_message(f"World '{world_name}' not found.")
