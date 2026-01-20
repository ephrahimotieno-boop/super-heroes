from config import app, db
from models import Episode, Guest, Appearance
from routes import *
import os


# Main entry point for the Flask application
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    # This function serves the React frontend build files.
    # It looks for index.html in the 'frontend/build' directory.
    frontend_build = os.path.join(os.path.dirname(__file__), 'frontend', 'build')
    index_file = os.path.join(frontend_build, 'index.html')
    
    if os.path.exists(index_file) and path:
        return os.path.join(frontend_build, path)
    elif os.path.exists(index_file):
        return open(index_file).read()
    else:
        # Fallback if the frontend hasn't been built yet
        return "Frontend not built. Run 'cd frontend && npm run build' first."


if __name__ == '__main__':
    app.run(debug=True, port=5005)
