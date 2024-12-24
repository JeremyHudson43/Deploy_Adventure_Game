from flask import Flask, render_template, request
import sys
import os
from pathlib import Path

# Get the absolute path to the src directory
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.append(str(src_dir))

# Now we can import from the src directory
from core.Game import Game
import threading
import queue

app = Flask(__name__, 
           template_folder=str(current_dir / 'templates'))

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Store game instances per session
games = {}
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
        session_id = request.remote_addr
        output_queue = queue.Queue()
        games[session_id] = Game()
        output_queues[session_id] = output_queue
        
        # Set up output capture
        flush_output, restore_stdout = capture_output(output_queue)
        
        try:
            # Initialize game
            games[session_id].setup()
            flush_output()
        finally:
            restore_stdout()
        
        # Collect all output
        output = ""
        while not output_queues[session_id].empty():
            output += output_queues[session_id].get()
        
        return output

    except Exception as e:
        app.logger.error(f"Error during game initialization: {str(e)}")
        return f"Error initializing game: {str(e)}", 500

@app.route('/command', methods=['POST'])
def process_command():
    try:
        session_id = request.remote_addr
        command = request.form.get('command', '').strip()
        
        if session_id not in games:
            return "Game session not found. Please refresh the page."
            
        game = games[session_id]
        output_queue = output_queues[session_id]
        
        # Set up output capture
        flush_output, restore_stdout = capture_output(output_queue)
        
        try:
            # Process command
            game.command_processor.process_command(command)
            game.boss_battle.trigger_battle()
            flush_output()
        finally:
            restore_stdout()
        
        # Collect all output
        output = ""
        while not output_queues[session_id].empty():
            output += output_queues[session_id].get()
        
        return output

    except Exception as e:
        app.logger.error(f"Error processing command: {str(e)}")
        return f"Error processing command: {str(e)}", 500

if __name__ == '__main__':
    # Ensure templates directory exists
    templates_dir = current_dir / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # For deployment environment, listen on all interfaces
    app.run(host='0.0.0.0', port=8080)
