import sys
import check_library

check_library.check_or_install_library('Flask')
check_library.check_or_install_library('Flask-Session')

from flask import Flask, render_template, jsonify, session
from flask_session import Session

import server_communication as server

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    session["modality"] = "AUTOMATIC"
    # Important create a local copy before using data to avoid race conditions
    with server.state_lock:
        state_copy = str(server.state)
    with server.valve_level_lock:
        valve_level_copy = str(server.valve_level)
    return render_template("index.html", state=state_copy, valve_level=valve_level_copy)

@app.route('/data')
def get_data():
    with server.water_levels_lock:
        water_levels_copy = server.water_levels[:]
        water_times_copy = server.water_times[:]
    with server.state_lock:
        state_copy = server.state
    with server.valve_level_lock:
        valve_level_copy = server.valve_level
    return jsonify({
        "connection": "OK" if server.connection else "ERROR",
        "state": state_copy,
        "valve_level": valve_level_copy,
        "water_levels": water_levels_copy,
        "water_times": water_times_copy
    })

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    elif len(sys.argv) == 1:
        host = "localhost"
    else:
        sys.exit("Invalid number of arguments, server address expected")
    server.start(host)
    app.run()
