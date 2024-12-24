from flask import Flask, render_template, request, jsonify
import sys
import os
import uuid
import queue
import logging
import traceback
from pathlib import Path
import pickle
import hashlib

# Add src dir to path and import Game
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.append(str(src_dir))
from core.Game import Game

# Initialize Flask app
app = Flask(__name__, template_folder=str(current_dir / 'templates'))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.debug = os.getenv("FLASK_ENV") == "development"

# Configure logging
logging.basicConfig(
   level=logging.DEBUG if app.debug else logging.INFO,
   format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Game state management 
games = {}
output_queues = {}

def get_client_id():
   """Generate unique client ID from IP and user agent"""
   client_str = f"{request.remote_addr}_{request.user_agent.string}"
   return hashlib.sha256(client_str.encode()).hexdigest()[:16]

def capture_output(output_queue):
   """Capture stdout for game output"""
   from io import StringIO
   old_stdout = sys.stdout
   string_io = StringIO()
   sys.stdout = string_io

   def flush_output():
       output = string_io.getvalue()
       if output:
           output_queue.put(output)
           string_io.truncate(0)
           string_io.seek(0)

   def restore_stdout():
       sys.stdout = old_stdout

   return flush_output, restore_stdout

def save_game_state(session_id):
    try:
        if session_id in games:
            game = games[session_id]
            saves_dir = Path('saves')
            saves_dir.mkdir(exist_ok=True)

            # Get full room path/ID instead of just name
            current_room_id = None
            if game.current_world and game.player.current_room:
                for room_id, room in game.current_world.rooms.items():
                    if room == game.player.current_room:
                        current_room_id = room_id
                        break

            state = {
                'player': {
                    'inventory': [item.name for item in game.player.inventory],
                    'current_room': current_room_id  # Store full room ID
                },
                'current_world': game.current_world.name if game.current_world else None,
                'puzzles': {
                    puzzle_id: {
                        'completed': puzzle.completed,
                        'completed_groups': list(getattr(puzzle, '_completed_groups', set()))
                    }
                    for puzzle_id, puzzle in game.current_world.puzzles.items()
                } if game.current_world else {}
            }

            with open(saves_dir / f"{session_id}.save", 'wb') as f:
                pickle.dump(state, f)

    except Exception as e:
        logger.error(f"Error saving game state: {str(e)}")

def load_game_state(session_id):
   try:
       save_path = Path('saves') / f"{session_id}.save"
       if not save_path.exists():
           return False

       with open(save_path, 'rb') as f:
           state = pickle.load(f)

       game = Game()
       game.setup()

       if state['current_world']:
           # Load world
           game.current_world = game.worlds.get(state['current_world'])
           if game.current_world:
               game.current_world.initialize(game.game_state)
               
               # Load inventory
               saved_items = state['player'].get('inventory', [])
               for item_name in saved_items:
                   for world_item in game.current_world.items.values():
                       if world_item.name == item_name:
                           game.player.inventory.add(world_item)
                           break

               # Load room location 
               room_id = state['player'].get('current_room')
               if room_id in game.current_world.rooms:
                   game.player.current_room = game.current_world.rooms[room_id]
                   game.player.state.current_room_id = room_id
                   game.player.state.current_world_id = state['current_world']

               # Load puzzle states
               for puzzle_id, puzzle_state in state.get('puzzles', {}).items():
                   if puzzle_id in game.current_world.puzzles:
                       puzzle = game.current_world.puzzles[puzzle_id]
                       puzzle.completed = puzzle_state.get('completed', False)
                       if hasattr(puzzle, '_completed_groups'):
                           puzzle._completed_groups = set(puzzle_state.get('completed_groups', []))
                       puzzle.game = game

       games[session_id] = game
       return True

   except Exception as e:
       logger.error(f"Error loading game state: {str(e)}")
       logger.error(traceback.format_exc()) 
       return False

@app.route('/', methods=['GET'])
def home():
   return render_template('index.html')

@app.route('/init_game', methods=['POST'])
def init_game():
    try:
        client_id = get_client_id()
        session_id = f"session_{client_id}"
        output_queue = queue.Queue()
        
        game_exists = load_game_state(session_id)
        if not game_exists:
            game = Game()
            games[session_id] = game
            game.setup()
        else:
            game = games[session_id]

        output_queues[session_id] = output_queue
        flush_output, restore_stdout = capture_output(output_queue)

        try:
            if not game_exists:
                game.intro()
            game.command_processor.look()
            flush_output()
        finally:
            restore_stdout()

        output = ""
        while not output_queue.empty():
            output += output_queue.get()

        save_game_state(session_id)

        return jsonify({
            'sessionId': session_id,
            'output': output
        })

    except Exception as e:
        logger.error(f"Error in init_game: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/command', methods=['POST'])
def process_command():
   try:
       data = request.get_json()
       session_id = data.get('sessionId')
       command = data.get('command', '').strip()

       if not session_id or session_id not in games:
           return jsonify({
               'error': 'Session expired',
               'output': 'Game session expired. Please refresh the page.'
           }), 404

       game = games[session_id]
       output_queue = output_queues[session_id]
       flush_output, restore_stdout = capture_output(output_queue)

       try:
           game.command_processor.process_command(command)
           game.boss_battle.trigger_battle()
           flush_output()
           save_game_state(session_id)
       finally:
           restore_stdout()

       output = ""
       while not output_queue.empty():
           output += output_queue.get()

       return jsonify({'output': output})

   except Exception as e:
       logger.error(f"Error in process_command: {str(e)}")
       return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
