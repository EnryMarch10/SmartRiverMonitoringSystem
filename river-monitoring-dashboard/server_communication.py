import logging
import time, socket, threading

RESPONSE_ACCEPT = "ACCEPTED"
RESPONSE_REJECT = "REJECT"

connection = False

lock_water_levels = threading.Lock()
lock_state = threading.Lock()
lock_valve_level = threading.Lock()

lock_modality = threading.Lock()
id_manual = None

# Shared data structure to hold received data
MAX_WATER_LEVELS = 10
water_levels = []
water_times = []
state = "UNKNOWN"
valve_level = "UNKNOWN"

def client_data(host):
    global lock_water_levels, water_levels, water_times, lock_state, state, lock_valve_level, valve_level, lock_modality, id_manual
    port = 57134
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    global connection
    try:
        server.connect((host, port))
        connection = True
        while True:
            data = server.recv(100)
            if data:
                message = data.decode()
                logging.info(f"[TCPClientData] New data: `{message}`")
                first_space_index = message.find(' ')
                last_space_index = message.rfind(' ')
                if first_space_index != -1 and last_space_index != -1:
                    if first_space_index != last_space_index:
                        if message[:first_space_index] == "water_level":
                            with lock_water_levels:
                                water_times.append(message[first_space_index + 1:last_space_index])
                                water_levels.append(message[last_space_index + 1:])
                                if len(water_levels) > MAX_WATER_LEVELS:
                                    water_levels = water_levels[-MAX_WATER_LEVELS:]
                                    water_times = water_times[-MAX_WATER_LEVELS:]
                        elif message[:first_space_index] == "mode":
                            address = message[first_space_index + 1:last_space_index]
                            modality = message[last_space_index + 1:]
                            with lock_modality:
                                if modality == "AUTOMATIC":
                                    id_manual = None
                                else:
                                    id_manual = address
                    else:
                        if message[:first_space_index] == "valve_level":
                            with lock_valve_level:
                                valve_level = message[first_space_index + 1:]
                        elif message[:first_space_index] == "state":
                            with lock_state:
                                state = message[first_space_index + 1:]
    except Exception as e:
        logging.warning(f"[TCPClientData] Failed with message: `{repr(e)}`")
    finally:
        connection = False
        try:
            server.close()
        except Exception as e:
            logging.error(f"[TCPClientData] Failed to close connection with message: `{repr(e)}`")

def client_set_modality(host, addr, modality):
    port = 57150
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    global lock_modality, id_manual
    result = False
    try:
        server.connect((host, port))
        server.sendall(str.encode(f"{addr} {modality}"))
        data = server.recv(50)
        if data:
            message = data.decode()
            if message == RESPONSE_ACCEPT:
                result = True
                if modality == "AUTOMATIC":
                    with lock_modality:
                        id_manual = None
                elif modality == "MANUAL":
                    with lock_modality:
                        id_manual = addr
    except Exception as e:
        logging.warning(f"[TCPClientModality] Failed with message: `{repr(e)}`")
    finally:
        try:
            server.close()
        except Exception as e:
            logging.error(f"[TCPClientModality] Failed to close connection with message: `{repr(e)}`")
        return result

def client_set_valve_level(host, addr, valve_level):
    port = 57183
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    result = False
    try:
        server.connect((host, port))
        server.sendall(str.encode(f"{addr} {valve_level}"))
        data = server.recv(50)
        if data:
            message = data.decode()
            if message == RESPONSE_ACCEPT:
                result = True
    except Exception as e:
        logging.warning(f"[TCPClientValveLevel] Failed with message: `{repr(e)}`")
    finally:
        try:
            server.close()
        except Exception as e:
            logging.error(f"[TCPClientValveLevel] Failed to close connection with message: `{repr(e)}`")
        return result

def connections_manager(host):
    t = threading.Thread(target=client_data, args=(host,), daemon=True)
    t.start()
    time.sleep(2)
    while True:
        if not t.is_alive():
            logging.info("[ClientDataConnectionManager] Thread data failed, trying to restart it...")
            t = threading.Thread(target=client_data, args=(host,), daemon=True)
            t.start()
        time.sleep(5)

def start(host):
    threading.Thread(target=connections_manager, args=(host,), daemon=True).start()
