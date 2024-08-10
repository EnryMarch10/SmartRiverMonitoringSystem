import logging
import sys, time, socket, threading

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
            data = server.recv(100)
            if data:
                message = data.decode()
                first_space_index = message.find(' ')
                last_space_index = message.rfind(' ')
                if first_space_index != -1 and last_space_index != -1:
                    if first_space_index != last_space_index:
                        if message[:first_space_index] == "water_level":
                            with water_levels_lock:
                                water_times.append(message[first_space_index + 1:last_space_index])
                                water_levels.append(message[last_space_index + 1:])
                                if len(water_levels) > MAX_WATER_LEVELS:
                                    water_levels = water_levels[-MAX_WATER_LEVELS:]
                                    water_times = water_times[-MAX_WATER_LEVELS:]
                    else:
                        if message[:first_space_index] == "state":
                            with state_lock:
                                state = message[first_space_index + 1:]
                        elif message[:first_space_index] == "valve_level":
                            with valve_level_lock:
                                valve_level = message[first_space_index + 1:]
            # time.sleep(0.1) # simulates delay
    except Exception as e:
        logging.info(f"[TCPClientData] Failed with message: `{repr(e)}`")
    finally:
        try:
            server.close()
        except Exception as e:
            logging.error(f"[TCPClientData] Failed to close connection with message: `{repr(e)}`")

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
            logging.info("[ConnectionsManager] Thread data failed, trying to restart it...")
            t = threading.Thread(target=_client_data, args=(host,), daemon=True)
            t.start()
            time.sleep(3)
            if t.is_alive():
                connection = True
        time.sleep(3)

def start(host):
    threading.Thread(target=_connections_manager, args=(host,), daemon=True).start()
