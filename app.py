from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    some_env_var = os.environ.get('SOME_ENV_VAR', '(missing)')
    return render_template('index.html', some_env_var=some_env_var)

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)