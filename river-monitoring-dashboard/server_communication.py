import sys, time, re, socket, threading
from datetime import datetime

connection = False

water_levels_lock = threading.Lock()
state_lock = threading.Lock()
valve_level_lock = threading.Lock()

# Shared data structure to hold received data
MAX_WATER_LEVELS = 10
water_levels = []
water_times = []
state = "UNKNOWN"
valve_level = "UNKNOWN"

def _client_data(host):
    global water_levels, water_times, state, valve_level, water_levels_lock, state_lock, valve_level_lock
    port = 57134
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.connect((host, port))
        while True:
            received = server.recv(1024)
            if received:
                x = re.split("\\s", received.decode())
                if len(x) == 2:
                    if x[0] == "water_level":
                        with water_levels_lock:
                            water_times.append(datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
                            water_levels.append(x[1])
                            if len(water_levels) > MAX_WATER_LEVELS:
                                water_levels = water_levels[-MAX_WATER_LEVELS:]
                                water_times = water_times[-MAX_WATER_LEVELS:]
                    elif x[0] == "state":
                        with state_lock:
                            state = x[1]
                    elif x[0] == "valve_level":
                        with valve_level_lock:
                            valve_level = x[1]
            time.sleep(0.1) # simulates delay
    except Exception as e:
        print(f"[TCPClientData] Failed with message: `{repr(e)}`", file=sys.stderr)
    finally:
        try:
            server.close()
        except Exception as e:
            print(f"[TCPClientData] Failed to close connection with message: `{repr(e)}`", file=sys.stderr)

def _connections_manager(host):
    global connection
    t = threading.Thread(target=_client_data, args=(host,), daemon=True)
    t.start()
    time.sleep(3)
    if t.is_alive():
        connection = True
    while True:
        if not t.is_alive():
            if connection:
                connection = False
            print("[ConnectionsManager] Thread data failed, trying to restart it...", file=sys.stderr)
            t = threading.Thread(target=_client_data, args=(host,), daemon=True)
            t.start()
            time.sleep(3)
            if t.is_alive():
                connection = True
        time.sleep(3)

def start(host):
    threading.Thread(target=_connections_manager, args=(host,), daemon=True).start()
