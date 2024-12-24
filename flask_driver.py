from flask import Flask, render_template, request
from core.Game import Game
from core.systems.DisplayManager import DisplayManager
import threading
import queue

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Store game instances per session (in a real app, use proper session management)
games = {}
output_queues = {}

class WebDisplayManager(DisplayManager):
    def __init__(self, output_queue):
        super().__init__()
        self.output_queue = output_queue

    def print_message(self, message):
        self.output_queue.put(f"{message}\n")

    def print_decorated(self, message):
        self.output_queue.put(f"\n{'='*60}\n{message}\n{'='*60}\n")

    def print_list(self, title, items, format_func=None):
        output = f"\n{title}:\n"
        if not items:
            output += f"  • No {title.lower()} here.\n"
        else:
            for item in items:
                formatted = format_func(item) if format_func else str(item)
                output += f"  • {formatted}\n"
        self.output_queue.put(output)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/init_game', methods=['POST'])
def init_game():
    session_id = request.remote_addr  # Use IP as simple session ID
    output_queue = queue.Queue()
    games[session_id] = Game()
    games[session_id].display = WebDisplayManager(output_queue)
    output_queues[session_id] = output_queue
    
    # Initialize game
    game_thread = threading.Thread(target=games[session_id].setup)
    game_thread.start()
    game_thread.join()
    
    # Collect all output
    output = ""
    while not output_queues[session_id].empty():
        output += output_queues[session_id].get()
    
    return output

@app.route('/command', methods=['POST'])
def process_command():
    session_id = request.remote_addr
    command = request.form.get('command', '').strip()
    
    if session_id not in games:
        return "Game session not found. Please refresh the page."
        
    game = games[session_id]
    output_queue = output_queues[session_id]
    
    # Process command in a thread to avoid blocking
    def process():
        game.command_processor.process_command(command)
        game.boss_battle.trigger_battle()
    
    game_thread = threading.Thread(target=process)
    game_thread.start()
    game_thread.join()
    
    # Collect all output
    output = ""
    while not output_queues[session_id].empty():
        output += output_queues[session_id].get()
    
    return output

if __name__ == '__main__':
    app.run(debug=True, port=8080)
