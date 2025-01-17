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

    from .routes import routes
    app.register_blueprint(routes, url_prefix='/')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
