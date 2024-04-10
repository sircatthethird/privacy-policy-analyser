from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Import route handlers
from save_url import save_url
from analyse_text import analyse_text

# Register route handlers
app.register_blueprint(save_url)
app.register_blueprint(analyse_text)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
