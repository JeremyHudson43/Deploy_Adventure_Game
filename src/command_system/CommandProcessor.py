from typing import List, Dict, Callable, Tuple
from command_system.MovementHandler import MovementManager
from command_system.InventoryHandler import InventoryManager
from command_system.DialogueHandler import DialogueManager
import adventurelib as adv
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # Only show warnings and errors

class CommandProcessor:
    def __init__(self, game, player, display_manager, game_state):
        self.game = game
        self.player = player
        self.display = display_manager
        self.game_state = game_state

        # Initialize managers
        self.movement = MovementManager(player, display_manager, game)
        self.inventory = InventoryManager(player, display_manager)
        self.dialogue = DialogueManager(player, display_manager, game)

        # Command handlers mapping
        self.commands = {
            "look": (self.look, []),
            "inventory": (self.inventory.show_inventory, []),
            "help": (self.print_help, []),
            "quit": (self.game.quit, []),
            "save": (self.handle_quick_save, []),
            "load": (self.handle_quick_load, []),
            "save game": (self.handle_named_save, []),
            "load game": (self.handle_load_game, []),
            "list saves": (self.handle_list_saves, []),
            "take": (self.handle_take, ["item_name"]),
            "get": (self.handle_take, ["item_name"]),
            "pick": (self.handle_take, ["item_name"]),
            "pick up": (self.handle_take, ["item_name"]),
            "drop": (self.handle_drop, ["item_name"]),
            "use": (self.handle_use, ["item_or_stairs"]),
            "talk": (self.handle_talk, ["npc_name"]),
            "go": (self.handle_go, ["direction"]),
            "teleport": (self.handle_teleport, ["world_name"]),
            "ask": (self.handle_ask, ["npc_name", "topic"]),
            "list worlds": (self.handle_list_worlds, []),
            "florbglorbule": (self.handle_dev_command, [])
        }

        self.awaiting_save_name = False
        self.awaiting_load_choice = False

    def look(self):
        room = self.player.current_room
        title = f"Room: {room.name}\n\n{room.description}"

        # Add puzzle-specific room descriptions
        room_id = self._get_room_id(room)
        if self.game.current_world and hasattr(self.game.current_world, 'puzzles'):
            for puzzle_id, puzzle in self.game.current_world.puzzles.items():
                if puzzle and puzzle.is_puzzle_room(room_id):
                    addon = puzzle.get_room_description_addon(room_id)
                    if addon:
                        title += f"\n\n{addon}"

        self.display.print_decorated(title)

        # Get exits including stairs
        exits = []

        # Handle normal exits
        for direction in room.exits():
            target_room = getattr(room, direction)
            if target_room:
                is_locked = False
                if self.game.current_world and hasattr(self.game.current_world, 'progression'):
                    target_room_id = self._get_room_id(target_room)
                    is_locked = not self.game.current_world.progression.is_room_accessible(
                        self.game.current_world.name, 
                        target_room_id
                    )
                
                target_room_name = target_room.name if hasattr(target_room, 'name') else str(target_room).split('/')[-1].replace('_', ' ').title()
                exit_desc = f"{direction.capitalize()} (leads to {target_room_name}"
                if is_locked:
                    exit_desc += " - LOCKED"
                exit_desc += ")"
                exits.append(exit_desc)
            else:
                exits.append(direction.capitalize())

        # Handle stairs
        if hasattr(room, 'stairs_up') and room.stairs_up:
            target_room = room.stairs_up
            is_locked = False
            if self.game.current_world and hasattr(self.game.current_world, 'progression'):
                target_room_id = target_room if isinstance(target_room, str) else self._get_room_id(target_room)
                is_locked = not self.game.current_world.progression.is_room_accessible(
                    self.game.current_world.name, target_room_id
                )
            
            target_room_name = target_room.split('/')[-1].replace('_', ' ').title() if isinstance(target_room, str) else target_room.name
            stair_desc = f"Up (leads to {target_room_name}"
            if is_locked:
                stair_desc += " - LOCKED"
            stair_desc += ")"
            exits.append(stair_desc)

        if hasattr(room, 'stairs_down') and room.stairs_down:
            target_room = room.stairs_down
            is_locked = False
            if self.game.current_world and hasattr(self.game.current_world, 'progression'):
                target_room_id = target_room if isinstance(target_room, str) else self._get_room_id(target_room)
                is_locked = not self.game.current_world.progression.is_room_accessible(
                    self.game.current_world.name, target_room_id
                )
            
            target_room_name = target_room.split('/')[-1].replace('_', ' ').title() if isinstance(target_room, str) else target_room.name
            stair_desc = f"Down (leads to {target_room_name}"
            if is_locked:
                stair_desc += " - LOCKED"
            stair_desc += ")"
            exits.append(stair_desc)

        # Sort exits alphabetically
        exits.sort()

        # Display exits and room contents
        self.display.print_list("Exits", exits)
        self.display.print_list("Items", room.items)

        if hasattr(room, 'npcs'):
            self.display.print_list("NPCs", room.npcs, lambda npc: npc.name)

    def handle_quick_save(self):
        """Handle quick save command"""
        success = self.game_state.save_game("quicksave")
        if success:
            self.display.print_message("Game saved.")
        else:
            self.display.print_message("Failed to save game.")

    def handle_quick_load(self):
        """Handle quick load command"""
        if self.game_state.load_game("quicksave"):
            self.look()
        else:
            self.display.print_message("No quicksave found.")

    def handle_named_save(self):
        """Start named save process"""
        self.display.print_message("Enter a name for your save:")
        self.awaiting_save_name = True

    def handle_load_game(self):
        """Start load game process"""
        saves = self.game_state.list_saves()
        if not saves:
            self.display.print_message("No saved games found.")
            return
            
        self.display.print_message("Available saves:")
        for i, save in enumerate(saves, 1):
            timestamp = save['timestamp']
            save_name = save['name']
            self.display.print_message(f"{i}. {save_name} ({timestamp})")
        
        self.display.print_message("\nEnter the number of the save to load:")
        self.awaiting_load_choice = True

    def handle_list_saves(self):
        """List all available saves"""
        saves = self.game_state.list_saves()
        if not saves:
            self.display.print_message("No saved games found.")
            return
            
        self.display.print_message("Available saves:")
        for i, save in enumerate(saves, 1):
            timestamp = save['timestamp']
            save_name = save['name']
            self.display.print_message(f"{i}. {save_name} ({timestamp})")

    def print_help(self):
        sections = [
            ("Basic Commands", [
                ("look", "Examine the current room"),
                ("inventory", "Check your inventory"),
                ("help", "Show this help message"),
                ("quit", "Exit the game")
            ]),
            ("Save/Load Commands", [
                ("save game", "Save game with custom name"),
                ("load game", "Load a saved game"),
                ("list saves", "List all saved games"),
                ("save", "Quick save"),
                ("load", "Quick load last save")
            ]),
            ("Navigation Commands", [
                ("go [direction]", "Move in a direction (north, south, east, west)"),
                ("use stairs [up/down]", "Use stairs to move between levels")
            ]),
            ("Interaction Commands", [
                ("take/get [item]", "Pick up an item"),
                ("drop [item]", "Drop an item from your inventory"),
                ("use [item]", "Use an item"),
                ("talk to [npc]", "Start a conversation with an NPC"),
                ("ask [npc] about [topic]", "Ask an NPC about a specific topic")
            ]),
            ("World Commands", [
                ("teleport [world]", "Teleport to a different world"),
                ("list worlds", "List all available worlds")
            ])
        ]

        if self.game.current_world and hasattr(self.game.current_world, 'puzzles'):
            room_id = self._get_room_id(self.player.current_room)
            for puzzle_id, puzzle in self.game.current_world.puzzles.items():
                if puzzle and puzzle.is_puzzle_room(room_id):
                    puzzle_commands = []
                    if hasattr(puzzle, 'commands'):
                        for cmd, info in puzzle.commands.items():
                            puzzle_commands.append((cmd, info))
                        if puzzle_commands:
                            sections.append((f"{puzzle_id.replace('_', ' ').title()} Commands", puzzle_commands))

        first_section = True
        for section, commands in sections:
            if not first_section:
                adv.say("")
            first_section = False
            self.display.print_help_section(section)
            for cmd, desc in commands:
                adv.say(f"• {cmd:<25} - {desc}")

    def handle_take(self, args: List[str]):
        item_name = ' '.join(args)
        self.inventory.take(item_name)

    def handle_drop(self, args: List[str]):
        item_name = ' '.join(args)
        self.inventory.drop(item_name)

    def handle_use(self, args: List[str]):
        if args and args[0].lower() == "stairs":
            direction = args[1].lower() if len(args) > 1 else None
            if direction in ["up", "down"]:
                self.movement.use_stairs(direction)
            else:
                self.display.print_message("Use stairs in which direction? (up/down)")
        else:
            self.inventory.use(' '.join(args))

    def handle_talk(self, args: List[str]):
        if args and args[0].lower() == "to":
            person_name = ' '.join(args[1:])
        else:
            person_name = ' '.join(args)
        self.dialogue.talk(person_name)

    def handle_go(self, args: List[str]):
        direction = args[-1] if args else ""
        if direction in ["up", "down"]:
            self.movement.use_stairs(direction)
        else:
            self.movement.go(direction)

    def handle_teleport(self, args: List[str]):
        if not args:
            worlds = [f"    {world_name}" for world_name in self.game.worlds.keys()]
            self.display.print_list("Available Worlds to Teleport To", worlds)
            self.display.print_message("Please specify a world to teleport to.")
            return

        world_name = ' '.join(args)
        if world_name.lower().startswith('to '):
            world_name = world_name[3:]

        target_world = None
        for name, world in self.game.worlds.items():
            if name.lower() == world_name.lower():
                target_world = world
                world_name = name
                break

        if target_world:
            target_world.initialize(self.game.game_state)
            self.game.current_world = target_world
            starting_room = target_world.get_starting_room()
            if starting_room:
                self.player.move_to(starting_room)
                self.display.print_message(f"Teleported to {world_name}.")
                self.look()
            else:
                self.display.print_message(f"Error: No starting room defined for world {world_name}")
        else:
            self.display.print_message(f"World '{world_name}' not found.")

    def handle_ask(self, args: List[str]):
        try:
            about_index = args.index("about")
            npc_name = " ".join(args[:about_index])
            topic = " ".join(args[about_index + 1:])
            self.dialogue.ask_npc(npc_name, topic)
        except ValueError:
            self.display.print_message("Usage: ask [person] about [topic]")

    def handle_list_worlds(self):
        worlds = [f"    {world_name}" for world_name in self.game.worlds.keys()]
        self.display.print_list("Available Worlds to Teleport To", worlds)
        self.display.print_message("Use 'teleport [world name]' to travel to a world.")

    def handle_dev_command(self):
        if self.game.current_world and hasattr(self.game.current_world, 'progression'):
            if self.game.current_world.progression.toggle_dev_mode("florbglorbule"):
                self.display.print_message("Dev mode activated - all rooms unlocked!")
            else:
                self.display.print_message("Dev mode activation failed.")

    def _get_room_id(self, room) -> str:
        if hasattr(room, 'id'):
            return room.id
        elif isinstance(room, str):
            return room
        else:
            current_world = self.game.current_world
            if not current_world:
                room_name = room.name.lower().replace(' ', '_').replace("'", "")
                return f"level_one/{room_name}"
                
            for room_path, world_room in current_world.rooms.items():
                if world_room == room:
                    return room_path
                    
            room_name = room.name.lower().replace(' ', '_').replace("'", "")
            return f"level_one/{room_name}"

    def process_command(self, command: str) -> None:
        # Handle save/load input states
        if self.awaiting_save_name:
            self.awaiting_save_name = False
            success = self.game_state.save_game(command)
            if success:
                self.display.print_message(f'Game saved as "{command}"')
            else:
                self.display.print_message("Failed to save game.")
            return

        if self.awaiting_load_choice:
            self.awaiting_load_choice = False
            try:
                choice = int(command)
                saves = self.game_state.list_saves()
                if 1 <= choice <= len(saves):
                    save_name = saves[choice-1]['name']
                    if self.game_state.load_game(save_name):
                        self.look()
                        self.display.print_message(f'Loaded save game "{save_name}"')
                    else:
                        self.display.print_message("Failed to load save game.")
                else:
                    self.display.print_message("Invalid save number.")
            except ValueError:
                self.display.print_message("Please enter a number.")
            return

        # Process normal commands
        parts = command.lower().split()
        matched_command = None

        # Match longest command first (e.g. "pick up" before "pick")
        for cmd in sorted(self.commands.keys(), key=lambda x: -len(x.split())):
            cmd_parts = cmd.split()
            if parts[:len(cmd_parts)] == cmd_parts:
                matched_command = cmd
                args = parts[len(cmd_parts):]
                break

        if matched_command:
            handler, expected_args = self.commands[matched_command]
            if expected_args:
                handler(args)
            else:
                handler()
        else:
            if self._check_puzzle_commands(command):
                return
            self.display.print_message("I don't understand that command.")

    def _check_puzzle_commands(self, command: str) -> bool:
        """Handle puzzle-specific commands."""
        if not (self.game.current_world and hasattr(self.game.current_world, 'puzzles')):
            return False

        room_id = self._get_room_id(self.player.current_room)
        command_lower = command.lower().strip()

        for puzzle_id, puzzle in self.game.current_world.puzzles.items():
            if hasattr(puzzle, 'is_puzzle_room') and puzzle.is_puzzle_room(room_id):
                # Pass any command to the puzzle handler when in a puzzle room
                success, message = puzzle.handle_command(
                    command=command_lower,
                    room_id=room_id,
                    inventory=list(self.player.inventory)
                )
                
                if message:  # Show message even if command wasn't successful
                    self.display.print_message(message)
                if success and hasattr(puzzle, 'check_completion'):
                    completion_check = puzzle.check_completion()
                    if completion_check[0]:
                        self.display.print_message(completion_check[1])
                return True

        return False