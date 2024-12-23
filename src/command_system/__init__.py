from .MovementHandler import MovementManager
from .InventoryHandler import InventoryManager
from .DialogueHandler import DialogueManager

# Add new commands to the help text
COMMANDS = {
    # ... existing commands ...
    'observe currents': 'Observe the air currents in the current room',
    'activate current': 'Activate the air current in the current room',
    'check currents': 'Check the status of all air currents'
}

__all__ = ['MovementManager', 'InventoryManager', 'DialogueManager'] 