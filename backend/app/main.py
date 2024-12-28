from flask import Flask
from .routes import hello
from .routes import suggestion

app = Flask(__name__)

app.register_blueprint(hello.bp)
app.register_blueprint(suggestion.bp)

if __name__ == "__main__":
    app.run()
