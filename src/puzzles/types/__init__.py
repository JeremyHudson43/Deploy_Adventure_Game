"""
Puzzle type implementations.
"""

import logging
import importlib
from typing import List

logger = logging.getLogger(__name__)

__all__: List[str] = []

# Try to import each puzzle type, skipping any that fail
puzzle_modules = [
    ('air_puzzle.AirLevelPuzzle', 'AirLevelPuzzle'),
    ('chiptune_puzzle.ChiptunePuzzle', 'ChiptunePuzzle'),
    ('steampunk_music_puzzle.SteampunkMusicPuzzle', 'SteampunkMusicPuzzle'),
    ('creative_convergence_puzzle.CreativeConvergencePuzzle', 'CreativeConvergencePuzzle'),
    ('fire_puzzle.FireLevelPuzzle', 'FireLevelPuzzle'),
    ('spirit_puzzle.SpiritLevelPuzzle', 'SpiritLevelPuzzle'),
    ('nostalgia_puzzle.NostalgiaPuzzle', 'NostalgiaPuzzle'),
    ('alternative_rock_puzzle.AlternativeRockPuzzle', 'AlternativeRockPuzzle'),
    ('water_puzzle.WaterLevelPuzzle', 'WaterLevelPuzzle'),
    ('earth_puzzle.EarthLevelPuzzle', 'EarthLevelPuzzle')
]

for module_path, class_name in puzzle_modules:
    try:
        module = importlib.import_module(f'.{module_path}', package='puzzles.types')
        globals()[class_name] = getattr(module, class_name)
        __all__.append(class_name)
        logger.info(f"Successfully imported {class_name}")
    except Exception as e:
        logger.warning(f"Failed to import {class_name}: {str(e)}")
        continue 