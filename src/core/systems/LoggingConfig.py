import logging

def setup_logging():
    """Configure logging for the game."""
    # Create formatters with more detailed information
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    
    # Create file handler
    file_handler = logging.FileHandler('game.log')
    file_handler.setLevel(logging.DEBUG)  # Set to DEBUG for maximum verbosity
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set to DEBUG for maximum verbosity
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Set to DEBUG for maximum verbosity
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Create loggers for different components
    world_logger = logging.getLogger('world')
    room_logger = logging.getLogger('room')
    command_logger = logging.getLogger('command')
    puzzle_logger = logging.getLogger('puzzle')
    
    return {
        'world': world_logger,
        'room': room_logger,
        'command': command_logger,
        'puzzle': puzzle_logger
    } 