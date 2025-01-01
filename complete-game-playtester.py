import subprocess
import sys
from pathlib import Path
import time
import threading
import queue
from typing import List, Dict
import os

class GameLevel:
    def __init__(self, name: str, commands: List[str]):
        self.name = name
        self.commands = commands

class GameAutomation:
    def __init__(self, game_path: str):
        self.script_dir = Path(__file__).parent
        self.game_path = game_path
        self.log_file = str(self.script_dir / "complete_game_playthrough.log")
        self.output_queue = queue.Queue()

    def execute_commands(self, game_process: subprocess.Popen, 
                        level: GameLevel, log_file) -> None:
        level_header = f"\n--- {level.name.upper()} LEVEL ---\n"
        log_file.write(level_header)
        print(level_header, end='')
        
        for command in level.commands:
            command_line = f"\n> {command}\n"
            log_file.write(command_line)
            print(command_line, end='')
            log_file.flush()
            game_process.stdin.write(f"{command}\n")
            game_process.stdin.flush()
            time.sleep(1)
            while not self.output_queue.empty():
                line = self.output_queue.get_nowait()
                log_file.write(line)
                print(line, end='')
                log_file.flush()
            time.sleep(0.5)

    def read_output(self, pipe, queue):
        try:
            for line in iter(pipe.readline, ''):
                queue.put(line)
                print(line, end='')
        except Exception as e:
            error_msg = f"Error reading output: {e}"
            queue.put(error_msg)
            print(error_msg)
        finally:
            pipe.close()

    def complete_elemental_conflux(self, game_process, log_file):
        """Complete all levels of Elemental Conflux world."""
        worlds_header = f"\n=== ELEMENTAL CONFLUX WORLD ===\n"
        log_file.write(worlds_header)
        print(worlds_header, end='')

        levels = [
            GameLevel("air", [
                "teleport to elemental conflux",
                "focus crystal",
                "go east",
                "align stars",
                "go east",
                "channel thunder",
                "go up"
            ]),
            GameLevel("earth", [
                "go west",  # To Chess Dojo
                "go west",  # To Toph's Caverns
                "sense crystal",
                "go east",  # Back to Chess Dojo
                "move piece",
                "go east",  # Back to Forge Hall
                "forge metal",
                "go up"
            ]),
            GameLevel("fire", [
                "channel flame",
                "go east",  # To Dragon Garden
                "steep tea",
                "go north",  # To Zuko's Fire
                "flow chi",
                "go up"
            ]),
            GameLevel("water", [
                "heal spirit",
                "go west",  # To Squirtle's Coast
                "ride surf",
                "go north",  # To Moana's Waves
                "read tide",
                "go up"
            ]),
            GameLevel("spirit", [
                "project realm",
                "go east",  # To Mount Pyres
                "honor ancestor",
                "go east",  # To Raava's Sanctuary
                "attune light",
                "take elemental shard"
            ])
        ]
        
        for level in levels:
            self.execute_commands(game_process, level, log_file)

    def complete_harmonic_nexus(self, game_process, log_file):
        """Complete all levels of Harmonic Nexus world."""
        log_file.write("\n=== HARMONIC NEXUS WORLD ===\n")
        print("\n=== HARMONIC NEXUS WORLD ===\n", end='')

        levels = [
            GameLevel("alternative_rock", [
                "teleport to harmonic nexus",
                "paint pattern",
                "go east",
                "play trumpet", 
                "go east",
                "capture moment",
                "go east", 
                "perform dance",
                "go up"
            ]),
            GameLevel("chiptune", [
                "compose melody",
                "go east",
                "sync beat",
                "go east",
                "play game",
                "go up"
            ]),
            GameLevel("steampunk", [
                "go west", # To Airship
                "conduct sail",
                "take resonance shard",
                "go west", # To Temporal Lab
                "reverse time",
                "go east", # Back to Airship
                "go east", # To Clockwork Stage
                "sync gear",
                ])
        ]
        
        for level in levels:
            self.execute_commands(game_process, level, log_file)

    def complete_whimsical_realm(self, game_process, log_file):
        """Complete all levels of Whimsical Realm world."""
        log_file.write("\n=== WHIMSICAL REALM WORLD ===\n")
        print("\n=== WHIMSICAL REALM WORLD ===\n", end='')

        levels = [
            GameLevel("creative", [
                "teleport to whimsical realm",
                "paint cloud",
                "go west",
                "fade reality",
                "go east",
                "go east",
                "present invention", 
                "go east",
                "build tower", 
                "go up"
            ]),
            GameLevel("nostalgia", [
                "collect boot",  # Wall-E's Wonderful World
                "go west",  # Queen of Hearts' Grim Garden Party
                "paint rose",  # Solve royal nostalgia
                "go west",  # Mad Hatter's Temporal Trap
                "pour tea",  # Solve wonderland mischief
                "go east",  # Queen of Hearts' Grim Garden Party
                "go east",  # Wall-E's Wonderful World
                "go east",  # Mr. Rogers' Nostalgic Nexus
                "share smile",  # Solve neighborly kindness
                "go up"  # Ascend stairs after solving all aspects
            ]),
            GameLevel("childhood", [
                "unite friend",  # Toaster puzzle
                "go east",  # To Blanka
                "spark thunder", # Blanka puzzle
                "go east", # To Pickleball
                "serve ball",  # Pickleball puzzle
                "go east", # To Sheetz
                "taste slushie", # Sheetz puzzle
                "take imagination shard",
                "3"
            ])
        ]

        for level in levels:
            self.execute_commands(game_process, level, log_file)

    def run_game(self):
        print(f"Starting complete game automation. Logs will be written to: {self.log_file}")
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            print("Starting game process...")
            os.chdir(str(Path(self.game_path).parent))
            game_process = subprocess.Popen(
                [sys.executable, self.game_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            output_thread = threading.Thread(
                target=self.read_output, 
                args=(game_process.stdout, self.output_queue)
            )
            output_thread.daemon = True
            output_thread.start()
            
            time.sleep(3)
            
            try:
                # Complete each world in sequence
                self.complete_elemental_conflux(game_process, f)
                self.complete_harmonic_nexus(game_process, f)
                self.complete_whimsical_realm(game_process, f)
                
                game_process.stdin.write("quit\n")
                game_process.stdin.flush()
                game_process.stdin.close()
                game_process.wait(timeout=5)
            
            except Exception as e:
                f.write(f"\nError: {str(e)}\n")
                game_process.kill()
            finally:
                game_process.terminate()
                output_thread.join()

def main():
    game_path = r"C:\Users\jer43\OneDrive\Documents\GitHub\Deploy_Adventure_Game\src\main.py"
    automation = GameAutomation(game_path)
    automation.run_game()

if __name__ == "__main__":
    main()