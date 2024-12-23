from typing import Optional, Dict, Any
import adventurelib as adv
from typing import Optional
from core.entities.NPC import NPC

import logging

logger = logging.getLogger(__name__)

class DialogueManager:
    def __init__(self, player, display_manager, game):
        self.player = player
        self.display = display_manager
        self.game = game

    def talk(self, person_name):
        """Initial talk command - shows description, greeting, and available topics."""
        if not hasattr(self.player.current_room, 'npcs'):
            self.display.print_message(f"Usage: ask [person] about [topic]")
            return
        
        npc = next((npc for npc in self.player.current_room.npcs 
                if npc.name.lower() == person_name.lower()), None)
        if not npc:
            self.display.print_message(f"Usage: ask [person] about [topic]")
            return
        
        # Format the NPC description
        npc_description = f"{npc.description}\n"
        
        # Get greeting message - handle both simple and nested formats
        greeting = None
        dialogue_data = getattr(npc, 'dialogue_data', getattr(npc, 'dialogue', {}))
        
        if 'greeting' in dialogue_data:
            greeting_data = dialogue_data['greeting']
            if isinstance(greeting_data, str):
                greeting = greeting_data
            elif isinstance(greeting_data, dict):
                # For NPCs with first_time/repeat greetings, use first_time
                greeting = greeting_data.get('first_time', greeting_data.get('repeat'))
        
        if greeting is None:
            greeting = "Hello!"  # Fallback greeting
            
        greeting_message = f"{npc.name} says:\n\n• \"{greeting}\""
        
        # Get available topics
        topics = []
        
        # Check for puzzle-specific topics
        if self.game.current_world and hasattr(self.game.current_world, 'puzzles'):
            for puzzle in self.game.current_world.puzzles.values():
                if hasattr(puzzle, 'get_npc_topics'):
                    puzzle_topics = puzzle.get_npc_topics(
                        npc.name, 
                        list(self.player.inventory)  # Pass actual Item objects
                    )
                    topics.extend(puzzle_topics)
        
        # Add standard topics from dialogue dictionary
        if 'topics' in dialogue_data:
            # New format with topics dictionary
            for key in dialogue_data['topics']:
                topic = key.replace('_', ' ')  # Format topic name
                if topic.startswith('about '):  # Strip 'about' prefix
                    topic = topic[6:]
                if topic not in topics:
                    topics.append(topic)
        else:
            # Old format with direct keys
            for key in dialogue_data:
                if key != 'greeting':  # Skip greeting since it's handled separately
                    topic = key.replace('_', ' ')  # Format topic name
                    if topic.startswith('about '):  # Strip 'about' prefix
                        topic = topic[6:]
                    if topic not in topics:
                        topics.append(topic)
        
        # Remove duplicates and sort
        topics = sorted(set(topics))
        
        # Combine NPC description, greeting, and topics into one formatted message
        topics_string = "\n• " + "\n• ".join(topics) if topics else ""
        combined_message = f"{npc_description}\n{greeting_message}"
        if topics:
            combined_message += f"\n\nYou can ask {npc.name} about:\n{topics_string}"
        
        self.display.print_decorated(combined_message)  # Output the entire NPC interaction as one decorated block!

    def ask_npc(self, npc_name, topic):
        """Handle asking NPC about a specific topic."""
        # Validate NPC presence
        npc = self._find_npc_in_room(npc_name)
        if not npc:
            return
            
        # Try puzzle dialogue first
        if self._try_puzzle_dialogue(npc, topic):
            return

        # Fall back to standard dialogue
        self._handle_standard_dialogue(npc, topic)

    def _find_npc_in_room(self, npc_name) -> Optional[NPC]:
        """Find an NPC in the current room by name."""
        if not hasattr(self.player.current_room, 'npcs'):
            self.display.print_message(f"There is no one named {npc_name} here.")
            return None

        npc = next((npc for npc in self.player.current_room.npcs 
                if npc.name.lower() == npc_name.lower()), None)
        if not npc:
            self.display.print_message(f"Usage: ask [person] about [topic]")
            return None
        
        return npc

    def _try_puzzle_dialogue(self, npc, topic) -> bool:
        """Attempt to handle dialogue through puzzle system.
        Returns True if puzzle dialogue was handled, False otherwise."""
        if not (self.game.current_world and hasattr(self.game.current_world, 'puzzles')):
            return False
        
        for puzzle in self.game.current_world.puzzles.values():
            if hasattr(puzzle, 'handle_npc_dialogue'):
                try:
                    dialogue = puzzle.handle_npc_dialogue(
                        npc.name,
                        topic,
                        list(self.player.inventory)
                    )
                    if dialogue is not None:
                        self.display.print_decorated(f"{npc.name} says:\n\n• \"{dialogue}\"")
                        return True
                except Exception as e:
                    logger.error(f"Error in puzzle dialogue handler: {e}")
        
        return False

    def _handle_standard_dialogue(self, npc, topic):
        """Handle standard NPC dialogue system."""
        # Remove 'the' and 'about' from the beginning of topics and normalize
        normalized_topic = topic.lower()
        if normalized_topic.startswith('the '):
            normalized_topic = normalized_topic[4:]
        if normalized_topic.startswith('about '):
            normalized_topic = normalized_topic[6:]
        normalized_topic = normalized_topic.replace(' ', '_')
        
        # Get dialogue data from either new or old format
        dialogue_data = getattr(npc, 'dialogue_data', getattr(npc, 'dialogue', {}))
        if not dialogue_data:
            self.display.print_message(f"{npc.name} has nothing to say about that topic.")
            return
            
        # First check topics dictionary if it exists
        if 'topics' in dialogue_data:
            # Try direct match
            if normalized_topic in dialogue_data['topics']:
                topic_data = dialogue_data['topics'][normalized_topic]
                self._display_topic_response(npc, topic_data)
                return
            # Try with about_ prefix
            about_topic = f"about_{normalized_topic}"
            if about_topic in dialogue_data['topics']:
                topic_data = dialogue_data['topics'][about_topic]
                self._display_topic_response(npc, topic_data)
                return
            
        # Then check direct keys (old format)
        if normalized_topic in dialogue_data:
            topic_data = dialogue_data[normalized_topic]
            self._display_topic_response(npc, topic_data)
            return
            
        # Finally check about_ prefix
        topic_key = f"about_{normalized_topic}"
        if topic_key in dialogue_data:
            topic_data = dialogue_data[topic_key]
            self._display_topic_response(npc, topic_data)
            return
        
        self.display.print_message(f"{npc.name} has nothing to say about that topic.")
        
    def _display_topic_response(self, npc, topic_data):
        """Helper method to display topic responses in a consistent format."""
        if isinstance(topic_data, str):
            self.display.print_decorated(f"{npc.name} says:\n\n• \"{topic_data}\"")
        elif isinstance(topic_data, dict):
            # Handle nested dialogue with state-based responses
            if 'no_items' in topic_data and not self.player.inventory:
                responses = [topic_data['no_items']]
            elif 'initial' in topic_data:
                responses = [topic_data['initial']]
            else:
                # Show all responses in the dictionary
                responses = []
                for subtopic, text in topic_data.items():
                    if isinstance(text, str):
                        responses.append(text)
                    elif isinstance(text, dict):
                        # Handle doubly nested dictionaries
                        for subsubtopic, subtext in text.items():
                            responses.append(subtext)
                
            # Format all responses with bullet points
            formatted_responses = [f"• \"{response}\"" for response in responses]
            self.display.print_decorated(f"{npc.name} says:\n\n" + "\n\n".join(formatted_responses))