from flask import Flask, send_from_directory
from .database import db
import os

def create_app():
    app = Flask(__name__)
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "instance", "summaries.db")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Delay importing setup_routes to avoid circular import
    from .services import setup_routes
    setup_routes(app)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        react_build_dir = os.path.join(base_dir, "../frontend/build")
        if path != "" and os.path.exists(os.path.join(react_build_dir, path)):
            return send_from_directory(react_build_dir, path)
        else:
            return send_from_directory(react_build_dir, "index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
