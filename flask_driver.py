from flask import Flask, render_template, request, jsonify
import sys
import os
import uuid
import queue
import threading
from pathlib import Path
import pickle

current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.append(str(src_dir))

from core.Game import Game

app = Flask(__name__, template_folder=str(current_dir / 'templates'))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

games = {}
game_states = {}
output_queues = {}

def capture_output(output_queue):
    import sys
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

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/init_game', methods=['POST'])
def init_game():
    try:
        data = request.get_json()
        session_id = str(uuid.uuid4())
        game = Game()
        games[session_id] = game
        
        output_queue = queue.Queue()
        output_queues[session_id] = output_queue
        
        flush_output, restore_stdout = capture_output(output_queue)
        
        try:
            # Initialize the game synchronously 
            game.display = game.display  # Ensure display is set
            game.setup()
            game.intro()  # Explicitly call intro
            game.command_processor.look()
            flush_output()
        except Exception as e:
            app.logger.error(f"Game initialization error: {str(e)}")
            return jsonify({
                'error': str(e),
                'output': f"Error initializing game: {str(e)}"
            }), 500
        finally:
            restore_stdout()
        
        output = ""
        while not output_queues[session_id].empty():
            output += output_queues[session_id].get()
        
        # Save initial state
        save_game_state(session_id)
        
        return jsonify({
            'sessionId': session_id,
            'output': output
        })

    except Exception as e:
        app.logger.error(f"Outer initialization error: {str(e)}")
        return jsonify({
            'error': str(e),
            'output': f"Failed to start game: {str(e)}"
        }), 500
def save_game_state(session_id):
    """Save game state using the game's built-in save system"""
    if session_id in games:
        game = games[session_id]
        saves_dir = Path('saves')
        saves_dir.mkdir(exist_ok=True)
        save_path = saves_dir / f"{session_id}.dat"
        
        game_state = {
            'player_state': game.player.serialize(),
            'world_state': {
                'current_world': game.current_world.name,
                'world_progress': game.game_state.world_progress
            }
        }
        
        with open(save_path, 'wb') as f:
            pickle.dump(game_state, f)

def load_game_state(session_id):
    """Load game state using the game's built-in save system"""
    save_path = Path('saves') / f"{session_id}.dat"
    if save_path.exists():
        with open(save_path, 'rb') as f:
            game_state = pickle.load(f)
            
        game = games[session_id]
        game.player.deserialize(game_state['player_state'])
        game.current_world = game.worlds[game_state['world_state']['current_world']]
        game.game_state.world_progress = game_state['world_state']['world_progress']
        game.current_world.initialize(game.game_state)
        return True
    return False

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
        return jsonify({
            'error': str(e),
            'output': f"Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
