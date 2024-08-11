from utils.logging_config import setup_logging

# Logger configuration has to be done before everything else
setup_logging()

import sys, logging, uuid
import utils.check_library as check_library

check_library.check_or_install_library('Flask')

from flask import Flask, make_response, render_template, jsonify, request


import server_communication as server

app = Flask(__name__)

host = "localhost"

@app.route('/')
def index():
    # Important create a local copy before using data to avoid race conditions
    with server.lock_state:
        state_copy = str(server.state)
    with server.lock_valve_level:
        valve_level_copy = str(server.valve_level)
    user_id = request.cookies.get('user_id')
    response = None
    if not user_id:
        response = make_response(render_template("index.html", state=state_copy, valve_level=valve_level_copy, modality="AUTOMATIC"))
        user_id = str(uuid.uuid4())
        response.set_cookie('user_id', user_id, max_age=60*60*24*365)
    else:
        with server.lock_modality:
            id = server.id_manual
        response = make_response(render_template("index.html", state=state_copy, valve_level=valve_level_copy, modality="MANUAL" if id == user_id else "AUTOMATIC", busy="No" if id is None else "Yes"))
    return response

@app.route('/data')
def get_data():
    with server.lock_water_levels:
        water_levels_copy = server.water_levels[:]
        water_times_copy = server.water_times[:]
    with server.lock_state:
        state_copy = server.state
    with server.lock_valve_level:
        valve_level_copy = server.valve_level
    with server.lock_modality:
        id = server.id_manual
    return jsonify({
        "connection": "OK" if server.connection else "ERROR",
        "state": state_copy,
        "valve_level": valve_level_copy,
        "water_levels": water_levels_copy,
        "water_times": water_times_copy,
        "modality": "MANUAL" if id == request.cookies.get('user_id') else "AUTOMATIC",
        "busy": "No" if id is None else "Yes"
    })

@app.route('/toggle_modality', methods=['POST'])
def toggle_modality():
    global host
    data = request.get_json()
    nextModality = data.get('mode')
    logging.debug(f"[ToggleModality] Trying to set modality to `{nextModality}`")
    result = server.client_set_modality(host, request.cookies.get('user_id'), nextModality)
    logging.debug(f"[ToggleModality] Result is `{result}`")
    return jsonify({
        "result": "OK" if result else "ERROR"
    })

@app.route('/set_valve_level', methods=['POST'])
def set_valve_level():
    global host
    data = request.get_json()
    result = False
    with server.lock_modality:
        modality = "MANUAL" if server.id_manual == request.cookies.get('user_id') else "AUTOMATIC"
    if modality == "MANUAL":
        valve_level = data.get('valve_level')
        logging.debug(f"[SetValveLevel] Trying to set valve level to `{valve_level}`")
        result = server.client_set_valve_level(host, request.cookies.get('user_id'), valve_level)
        logging.debug(f"[SetValveLevel] Result is `{result}`")
    return jsonify({
        "result": "OK" if result else "ERROR"
    })

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    elif len(sys.argv) != 1:
        sys.exit("Invalid number of arguments, server address expected")
    server.start(host)
    app.run()
