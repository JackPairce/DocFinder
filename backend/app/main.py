from flask import Flask
from .routes import hello

app = Flask(__name__)

app.register_blueprint(hello.bp)

if __name__ == '__main__':
    app.run()