from flask import Flask
from flask_cors import CORS
from .routes import hello
from .routes import suggestion

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:3000",
            "methods": ["POST"],
        }
    },
)

app.register_blueprint(hello.bp)
app.register_blueprint(suggestion.bp)

if __name__ == "__main__":
    app.run()
