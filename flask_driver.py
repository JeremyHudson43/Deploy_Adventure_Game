from flask import Flask, render_template, request
import os

# Import your game's core logic
# from adventure_game_adventure_lib.src.core.Game import Game

# Create the Flask application
app = Flask(__name__)

# Initialize the game
game = Game()

@app.route('/', methods=['GET', 'POST'])
def adventure():
    """
    Main route for Tezzeret's Surreal Adventure.
    Handles user input and game state.
    """
    if request.method == 'POST':
        # Get user input
        user_input = request.form['message']

        # Process the input through your game's logic
        response = game.process_command(user_input)

        # Return the updated game state and response to the template
        return render_template('adventure.html', user_input=user_input, response=response)
    else:
        # Render the initial game state
        intro_message = game.get_intro()
        return render_template('adventure.html', user_input=None, response=intro_message)

if __name__ == '__main__':
    # On Railway, the port is usually set in the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
