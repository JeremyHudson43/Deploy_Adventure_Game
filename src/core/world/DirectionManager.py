from adventurelib import Room

def initialize_directions():
    """Initialize all available directions for rooms."""
    # Standard cardinal directions are already added by adventurelib:
    # Room.add_direction('north', 'south')
    # Room.add_direction('east', 'west')
    
    # Add vertical directions
    Room.add_direction('up', 'down') 