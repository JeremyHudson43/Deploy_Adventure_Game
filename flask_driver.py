from flask import Flask, render_template, request, jsonify
import sys
import os
import uuid
import queue
import logging
import traceback
from pathlib import Path
import pickle

# Add the source directory to sys.path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.append(str(src_dir))

# Import the Game class
from core.Game import Game

# Initialize Flask app
app = Flask(__name__, template_folder=str(current_dir / 'templates'))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Enable debug mode based on environment
app.debug = os.getenv("FLASK_ENV") == "development"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if app.debug else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Globals for managing game sessions
games = {}
output_queues = {}

# Utility: Capture stdout for game output
def capture_output(output_queue):
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

# Route: Home Page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Route: Initialize Game
@app.route('/init_game', methods=['POST'])
def init_game():
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        output_queue = queue.Queue()

        # Attempt to load existing game state
        if session_id and load_game_state(session_id):
            game = games[session_id]
            game.command_processor.look()
        else:
            # Start a new game session
            session_id = str(uuid.uuid4())
            game = Game()
            games[session_id] = game
            game.setup()

        output_queues[session_id] = output_queue
        flush_output, restore_stdout = capture_output(output_queue)

        try:
            flush_output()
        finally:
            restore_stdout()

        # Collect output from the game
        output = ""
        while not output_queue.empty():
            output += output_queue.get()

        save_game_state(session_id)

        return jsonify({
            'sessionId': session_id,
            'output': output
        })

    except Exception as e:
        logger.error("Error in init_game: %s", traceback.format_exc())
        return jsonify({'error': str(e), 'output': f"Error: {str(e)}"}), 500

# Utility: Save Game State
def save_game_state(session_id):
    try:
        if session_id in games:
            game = games[session_id]
            saves_dir = Path('saves')
            saves_dir.mkdir(exist_ok=True)

            state = {
                'player': game.player.serialize(),
                'current_world': game.current_world.name if game.current_world else None,
                'worlds': {name: world.serialize() for name, world in game.worlds.items()},
                'game_state': game.game_state.serialize() if hasattr(game.game_state, 'serialize') else None
            }

            with open(saves_dir / f"{session_id}.save", 'wb') as f:
                pickle.dump(state, f)
    except Exception as e:
        logger.error("Error in save_game_state: %s", traceback.format_exc())

def load_game_state(session_id):
    try:
        save_path = Path('saves') / f"{session_id}.save"
        if not save_path.exists():
            return False

        with open(save_path, 'rb') as f:
            state = pickle.load(f)

        game = Game()
        game.player.deserialize(state['player'])

        if state['current_world']:
            game.current_world = game.worlds.get(state['current_world'])
            if game.current_world is None:
                raise ValueError(f"World '{state['current_world']}' not found.")

            current_room_name = state['player'].get('current_room')
            game.player.current_room = game.current_world.rooms.get(current_room_name)
            if game.player.current_room is None:
                raise ValueError(f"Room '{current_room_name}' not found in world '{state['current_world']}'.")

            game.current_world.initialize(game.game_state)

        games[session_id] = game
        return True
    except Exception as e:
        logger.error("Error in load_game_state: %s", traceback.format_exc())
        return False

# Route: Process Command
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
        logger.error("Error in process_command: %s", traceback.format_exc())
        return jsonify({
            'error': str(e),
            'output': f"Error: {str(e)}"
        }), 500

# Main Entry Point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
