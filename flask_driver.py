from flask import Flask, render_template, request, jsonify
import sys
import os
import uuid
import queue
import threading
from pathlib import Path

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
       session_id = str(uuid.uuid4())
       output_queue = queue.Queue()
       output_queues[session_id] = output_queue
       
       game = Game()
       games[session_id] = game
       
       flush_output, restore_stdout = capture_output(output_queue)
       
       try:
           game.setup()
           flush_output()
       finally:
           restore_stdout()
           game_states[session_id] = game
       
       output = ""
       while not output_queues[session_id].empty():
           output += output_queues[session_id].get()
       
       return jsonify({
           'sessionId': session_id,
           'output': output
       })

   except Exception as e:
       app.logger.error(f"Error during game initialization: {str(e)}")
       return jsonify({
           'error': str(e),
           'output': "Starting new game...\n"
       })

@app.route('/command', methods=['POST'])
def process_command():
   try:
       data = request.get_json()
       session_id = data.get('sessionId')
       command = data.get('command', '').strip()
       
       if not session_id or session_id not in games:
           return jsonify({
               'error': 'Session not found',
               'output': 'Game session expired. Please refresh the page.'
           }), 404
           
       game = games[session_id]
       output_queue = output_queues.get(session_id, queue.Queue())
       output_queues[session_id] = output_queue
       
       flush_output, restore_stdout = capture_output(output_queue)
       
       try:
           game.command_processor.process_command(command)
           game.boss_battle.trigger_battle()
           flush_output()
           game_states[session_id] = game
           
       finally:
           restore_stdout()
       
       output = ""
       while not output_queue.empty():
           output += output_queue.get()
       
       return jsonify({'output': output})

   except Exception as e:
       app.logger.error(f"Error processing command: {str(e)}")
       return jsonify({
           'error': str(e),
           'output': f"Error: {str(e)}"
       }), 500

@app.route('/save', methods=['POST'])
def save():
   session_id = request.json.get('sessionId')
   if session_id and session_id in games:
       game_states[session_id] = games[session_id]
       return jsonify({'success': True})
   return jsonify({'success': False})

@app.route('/load', methods=['POST'])
def load():
   try:
       session_id = request.json.get('sessionId')
       if session_id and session_id in game_states:
           game = game_states[session_id]
           games[session_id] = game
           
           output_queue = queue.Queue()
           output_queues[session_id] = output_queue
           flush_output, restore_stdout = capture_output(output_queue)
           
           try:
               game.command_processor.look()
               flush_output()
           finally:
               restore_stdout()
               
           output = ""
           while not output_queue.empty():
               output += output_queue.get()
               
           return jsonify({
               'success': True,
               'output': output
           })
           
       return jsonify({
           'success': False,
           'output': 'No saved game found'
       })
       
   except Exception as e:
       return jsonify({
           'success': False,
           'error': str(e),
           'output': f"Error loading game: {str(e)}"
       })

if __name__ == '__main__':
   templates_dir = current_dir / 'templates'
   templates_dir.mkdir(exist_ok=True)
   app.run(host='0.0.0.0', port=8080)
