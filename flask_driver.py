from flask import Flask, render_template, request, jsonify
import sys
import os
import uuid
import queue
import threading
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.append(str(src_dir))

from core.Game import Game

app = Flask(__name__, 
          template_folder=str(current_dir / 'templates'))

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Store game instances and states
games = {}
game_states = {}
output_queues = {}

def capture_output(output_queue):
   """Captures printed output and puts it in the queue"""
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
        existing_session_id = data.get('sessionId')
        
        if existing_session_id and existing_session_id in game_states and game_states[existing_session_id] is not None:
            session_id = existing_session_id
            games[session_id] = game_states[session_id]
        else:
            # Create new session if existing one not found or invalid
            session_id = str(uuid.uuid4())
            games[session_id] = Game()
            games[session_id].setup()  # Initialize new game immediately
            game_states[session_id] = games[session_id]
            
        output_queue = queue.Queue()
        output_queues[session_id] = output_queue
        flush_output, restore_stdout = capture_output(output_queue)
        
        try:
            games[session_id].command_processor.look()
            flush_output()
        finally:
            restore_stdout()
        
        output = ""
        while not output_queues[session_id].empty():
            output += output_queues[session_id].get()
        
        return jsonify({
            'sessionId': session_id,
            'output': output
        })

    except Exception as e:
        app.logger.error(f"Error during game initialization: {str(e)}")
        # Clear potentially corrupted session
        if 'session_id' in locals() and session_id in game_states:
            del game_states[session_id]
        return jsonify({
            'error': str(e),
            'output': f"Error initializing game: {str(e)}"
        }), 500

@app.route('/command', methods=['POST'])
def process_command():
   try:
       data = request.get_json()
       session_id = data.get('sessionId')
       command = data.get('command', '').strip()
       
       if session_id not in games:
           return jsonify({
               'error': 'Game session not found. Please refresh the page.',
               'output': 'Game session not found. Please refresh the page.'
           }), 404
           
       game = games[session_id]
       output_queue = output_queues[session_id]
       
       flush_output, restore_stdout = capture_output(output_queue)
       
       try:
           game.command_processor.process_command(command)
           game.boss_battle.trigger_battle()
           flush_output()
           
           # Save state after command
           game_states[session_id] = game
           
       finally:
           restore_stdout()
       
       output = ""
       while not output_queues[session_id].empty():
           output += output_queues[session_id].get()
       
       return jsonify({'output': output})

   except Exception as e:
       app.logger.error(f"Error processing command: {str(e)}")
       return jsonify({
           'error': str(e),
           'output': f"Error processing command: {str(e)}"
       }), 500

@app.route('/save_game', methods=['POST'])
def save_game():
   try:
       session_id = request.json.get('sessionId')
       if session_id in games:
           game_states[session_id] = games[session_id]
           return jsonify({'success': True})
       return jsonify({'success': False, 'error': 'Session not found'}), 404
   except Exception as e:
       return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
   templates_dir = current_dir / 'templates'
   templates_dir.mkdir(exist_ok=True)
   
   app.run(host='0.0.0.0', port=8080)
