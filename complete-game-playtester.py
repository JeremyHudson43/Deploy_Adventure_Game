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
                "look",
                "focus crystal",
                "go east",
                "look",
                "align stars",
                "go east",
                "look",
                "channel thunder",
                "go up"
            ]),
            GameLevel("earth", [
                "look",
                "go west",  # To Chess Dojo
                "look",
                "go west",  # To Toph's Caverns
                "look",
                "sense crystal",
                "go east",  # Back to Chess Dojo
                "look",
                "move piece",
                "go east",  # Back to Forge Hall
                "look", 
                "forge metal",
                "go up"
            ]),
            GameLevel("fire", [
                "look",
                "channel flame",
                "go east",  # To Dragon Garden
                "look",
                "steep tea",
                "go north",  # To Zuko's Fire
                "look",
                "flow chi",
                "go up"
            ]),
            GameLevel("water", [
                "look",
                "heal spirit",
                "go west",  # To Squirtle's Coast
                "look",
                "ride surf",
                "go north",  # To Moana's Waves
                "look",
                "read tide",
                "go up"
            ]),
            GameLevel("spirit", [
                "look",
                "project realm",
                "go east",  # To Mount Pyres
                "look",
                "honor ancestor",
                "go east",  # To Raava's Sanctuary
                "look",
                "attune light",
                "look",
                "take elemental shard"
            ])
        ]
        
        for level in levels:
            self.execute_commands(game_process, level, log_file)

    def complete_harmonic_nexus(self, game_process, log_file):
        """Complete all levels of Harmonic Nexus world."""
        worlds_header = f"\n=== HARMONIC NEXUS WORLD ===\n"
        log_file.write(worlds_header)
        print(worlds_header, end='')

        levels = [
            GameLevel("alternative_rock", [
                "teleport to harmonic nexus",
                "look",
                "paint pattern",  # Emotional resonance in Trench Terminal
                "go east",
                "look",
                "play trumpet",  # Energetic fusion in AJR Boulevard
                "go east",
                "look",
                "capture moment",  # Visual storytelling in Saint Motel
                "go east",
                "look",
                "perform dance",  # Theatrical performance in Panic Ballroom
                "go up"
            ]),
            GameLevel("chiptune", [
                "look",
                "compose melody",  # At Supergiant Studio
                "go east",
                "look", 
                "sync beat",  # At Qumu Oasis
                "go east",
                "look",
                "play game",  # At Snail's House
                "go up"
            ]),
            GameLevel("steampunk", [
                "go west",  # To Temporal Lab first!
                "look",
                "reverse time", 
                "go east",  # To Airship
                "look",
                "conduct wind",
                "go east",  # To Clockwork Stage
                "look",
                "sync gear",
                "look",
                "take resonance fragment" 
            ])]
        
        for level in levels:
            self.execute_commands(game_process, level, log_file)

    def complete_whimsical_realm(self, game_process, log_file):
        """Complete all levels of Whimsical Realm world."""
        worlds_header = f"\n=== WHIMSICAL REALM WORLD ===\n"
        log_file.write(worlds_header)
        print(worlds_header, end='')

        levels = [
            GameLevel("creative", [
                "teleport to whimsical realm",
                "look",
                "paint cloud",
                "go west",  # To Cheshire Cat
                "look",
                "fade reality",
                "go east",  # Back to Bob Ross
                "go east",  # To Megamind
                "look",
                "present invention",
                "go east",  # To Lego City
                "look",
                "build tower",
                "go up"  # To Mad Hatter's
            ]),
            GameLevel("nostalgia", [
                "look",
                "pour tea",  # Mad Hatter puzzle part 1
                "go west",  # To Queen of Hearts (from map)
                "look",
                "paint rose",  # Queen puzzle part 2
                "go east",  # To WALL-E's World
                "look",
                "collect treasure",  # WALL-E puzzle part 3
                "go east",  # From WALL-E to Mr. Rogers
                "look",
                "share smile",  # Rogers puzzle part 4 - completes level
                "go up"  # To Brave Little Toaster
            ]),
            GameLevel("childhood", [
                "look",
                "unite friend",  # Toaster puzzle part 1
                "go east",  # To Blanka's Jungle
                "look",
                "spark thunder",  # Blanka puzzle part 2
                "go east",  # To Pickleball Court
                "look",
                "serve ball",  # Pickleball puzzle part 3
                "go east",  # To Sheetz Station
                "look",
                "taste snack",  # Sheetz puzzle part 4
                "look",
                "take imagination shard fragment"
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