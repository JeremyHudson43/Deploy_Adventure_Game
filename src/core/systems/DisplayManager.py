import adventurelib as adv
import time

class DisplayManager:
    def __init__(self, line_length=60):
        self.line_length = line_length

    def print_line(self, char="-"):
        """Print a line without extra newlines"""
        adv.say(char * self.line_length)

    def print_section(self, title):
        adv.say("")  # Add an empty line before the section
        self.print_line()
        adv.say(title.center(self.line_length))
        self.print_line()
        adv.say("")  # Add an empty line after the section

    def print_decorated(self, message, char="="):
        adv.say("")  # Add an empty line before the decorated message
        self.print_line(char)
        for line in message.split('\n'):
            adv.say(line.center(self.line_length))
        self.print_line(char)
        adv.say("")  # Add an empty line after the decorated message

    def print_message(self, message):
        adv.say("")  # Add an empty line before the message
        self.print_line()
        adv.say(message)
        self.print_line()
        adv.say("")  # Add an empty line after the message

    def format_text(self, text):
        """Format text by replacing underscores with spaces and capitalizing appropriately"""
        if isinstance(text, str):
            return text.replace('_', ' ').title()
        return text

    def print_list(self, title, items, format_func=None):
        def print_empty_message():
            base_msg = title.lower() if title.lower() in ["items", "exits"] else title
            adv.say(f"  • There are no {base_msg} here.")
        
        def format_item(item):
            if isinstance(item, str):
                if item.startswith('•'):
                    return f"  {item}"
                if "leads to" in item.lower() or "portal to" in item.lower():
                    return f"  • {item}"
                formatted = format_func(item) if format_func else self.format_text(str(item))
                return f"  • {formatted}"
            return f"  • {format_func(item) if format_func else self.format_text(str(item))}"

        # Always print title with appropriate formatting
        adv.say("")  # Space before section
        if title == "Your inventory":
            self.print_line()
            adv.say(f"{title}:")
            self.print_line()
        elif title == "Available Worlds to Teleport To":
            self.print_line()
            adv.say(title)
            self.print_line()
        else:
            adv.say(f"{title}:")  # Just print title with colon
        
        # Handle empty lists
        if not items:
            print_empty_message()
            adv.say("")
            return
        
        # Print items
        for item in items:
            formatted_item = format_item(item)
            adv.say(formatted_item)
        
        # Add spacing after list if not "Available Worlds"
        if title != "Available Worlds to Teleport To":
            adv.say("")

    def print_simple_message(self, message):
        adv.say("")  # Add an empty line before the simple message
        adv.say(f"{message}")
        adv.say("")  # Add an empty line after the simple message

    def print_help_section(self, title):
        """Special method for printing help sections without extra newlines"""
        self.print_line()
        adv.say(title)
        self.print_line()