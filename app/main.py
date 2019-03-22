import os
import waitress
from flask import Flask, render_template, request


def start():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9876, debug=True)


if __name__ == '__main__':
    start()
