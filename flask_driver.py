from flask import Flask, render_template, request

# Create Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Render the main page and handle user input.
    """
    if request.method == 'POST':
        user_input = request.form['message']
        # Placeholder response; replace with your logic later
        response = f"You entered: {user_input}"
        return render_template('index.html', user_input=user_input, response=response)
    else:
        # Initial load
        return render_template('index.html', user_input=None, response=None)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))  # Use PORT env variable for Railway
    app.run(host='0.0.0.0', port=port)
