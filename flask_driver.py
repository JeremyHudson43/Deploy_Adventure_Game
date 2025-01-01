from flask import Flask, render_template, request, jsonify
import sys
import os
import queue
import logging
import traceback
from pathlib import Path
import pickle
import hashlib
import datetime

# Add src directory to path
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
games = {}  # Store instantiated games
output_queues = {}  # Store output queues for each game

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

def save_game_state(session_id, save_name=None):
    """Save game state to file"""
    try:
        if session_id in games:
            game = games[session_id]
            saves_dir = Path('saves')
            saves_dir.mkdir(exist_ok=True)

            # Build state object
            state = {
                'metadata': {
                    'save_name': save_name or session_id,
                    'timestamp': datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
                    'version': '1.0'
                },
                'game_state': game.game_state.serialize(),  # Serialize game state
                'player_state': game.player.serialize(),  # Serialize player state
                'world_state': game.current_world.serialize() if game.current_world else None,  # Serialize world
            }

            # Generate filename and save
            timestamp = state['metadata']['timestamp']
            filename = f"{save_name or session_id}_{timestamp}.save"
            with open(saves_dir / filename, 'wb') as f:
                pickle.dump(state, f)

            return True

    except Exception as e:
        logger.error(f"Error saving game state: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def load_game_state(session_id, save_name):
    """Load game state from file and initialize a new Game instance."""
    try:
        saves_dir = Path('saves')
        
        # Find specified save file
        pattern = f"{save_name}_*.save"
        save_files = list(saves_dir.glob(pattern))
        if not save_files:
            return None

        save_path = max(save_files, key=lambda p: p.stat().st_mtime)

        with open(save_path, 'rb') as f:
            state = pickle.load(f)

        # Create and setup new game
        game = Game()
        game.deserialize(state)
        game.game_state.deserialize(state['game_state'])
        game.player.deserialize(state['player_state'])
        game.current_world.deserialize(state['world_state'])

        games[session_id] = game
        return game

    except Exception as e:
        logger.error(f"Error loading game state: {str(e)}")
        logger.error(traceback.format_exc())
        return None
    
@app.route('/')
def home():
    """Render the game interface"""
    return render_template('index.html')

@app.route('/init_game', methods=['POST'])
def init_game():
    """Initialize a new game session."""
    try:
        client_id = get_client_id()
        session_id = f"session_{client_id}"
        
        # Only create a new game if one doesn't already exist for the session
        if session_id not in games:
            game = Game()
            games[session_id] = game
        else:
            game = games[session_id] # Get the existing game instance

        output_queue = queue.Queue()
        output_queues[session_id] = output_queue
        flush_output, restore_stdout = capture_output(output_queue)

        try:
            game.intro()
            flush_output()
        finally:
            restore_stdout()

        output = ""
        while not output_queue.empty():
            output += output_queue.get()

        return jsonify({
            'sessionId': session_id,
            'output': output
        })

    except Exception as e:
        logger.error(f"Error in init_game: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'output': f"Error initializing game: {str(e)}\nPlease contact the administrator."
        }), 500
    
@app.route('/command', methods=['POST'])
def process_command():
    """Process game commands."""
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        command = data.get('command', '').strip()

        if not session_id or session_id not in games:
            return jsonify({'error': 'Session expired', 'output': 'Game session expired or not initialized.'}), 404

        game = games[session_id]  # Retrieve the game instance
        output_queue = output_queues[session_id]
        flush_output, restore_stdout = capture_output(output_queue)

        output = ""

        try:
            # Let the command processor handle all commands
            game.command_processor.process_command(command)
            flush_output()

            # Capture any additional output
            while not output_queue.empty():
                output += output_queue.get()

        finally:
            restore_stdout()

        return jsonify({'output': output})

    except Exception as e:
        logger.error(f"Error in process_command: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'output': "An error occurred while processing the command. Please try again."
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))