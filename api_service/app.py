from flask import Flask
from api_service.routes import register_routes

def create_app():
    app = Flask(__name__)
    
    # Register your API routes from routes.py
    register_routes(app)
    
    return app

if __name__ == "__main__":
    app = create_app()
    
    # Start the Flask server
    app.run(host="0.0.0.0", port=5000, debug=True)
