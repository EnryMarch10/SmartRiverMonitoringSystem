import logging
import threading, time, socket
import atomic_counter
from controller import MyController
from data import Data, MySharedData

RESPONSE_ACCEPT = "ACCEPTED"
RESPONSE_REJECT = "REJECT"

N_CONNS_LIMIT = 5

n_connections_data = atomic_counter.AtomicCounter()
n_connections_modality = atomic_counter.AtomicCounter()
n_connections_valve_level = atomic_counter.AtomicCounter()

DELAY = 0.2 # s

def server_data(client: socket.socket, address):
    logging.debug("[TCPServerData] Client " + str(address) + " has connected")
    sent_sampling_time = sent_state = sent_valve_level = sent_modality = None
    try:
        while True:
            sampling_time, water_level, state, valve_level, modality, modality_address = MySharedData.get_dashboard_data()
            if sent_sampling_time != sampling_time:
                sendMessage = f"water_level {sampling_time} {water_level}"
                logging.debug(f"[TCPServerData] Sending `{sendMessage}`")
                client.sendall(str.encode(sendMessage))
            if sent_state != state:
                if sent_sampling_time != sampling_time:
                    # This seems to avoid strange multi packets loss
                    # It's possible that you have to increase the
                    # time in order to make it work
                    time.sleep(DELAY)
                sendMessage = f"state {state}"
                logging.debug(f"[TCPServerData] Sending `{sendMessage}`")
                client.sendall(str.encode(sendMessage))
            if sent_valve_level != valve_level:
                if sent_sampling_time != sampling_time or sent_state != state:
                    # This seems to avoid strange multi packets loss
                    # It's possible that you have to increase the
                    # time in order to make it work
                    time.sleep(DELAY)
                sendMessage = f"valve_level {valve_level}"
                logging.debug(f"[TCPServerData] Sending `{sendMessage}`")
                client.sendall(str.encode(sendMessage))
            if sent_modality != modality:
                if sent_sampling_time != sampling_time or sent_state != state or sent_valve_level != valve_level:
                    # This seems to avoid strange multi packets loss
                    # It's possible that you have to increase the
                    # time in order to make it work
                    time.sleep(DELAY)
                if modality_address is None:
                    modality_address = "UNKNOWN"
                sendMessage = f"mode {modality_address} {modality}"
                logging.debug(f"[TCPServerData] Sending `{sendMessage}`")
                client.sendall(str.encode(sendMessage))
            sent_sampling_time = sampling_time
            sent_state = state
            sent_valve_level = valve_level
            sent_modality = modality
            time.sleep(0.5)
    except Exception as e:
        logging.warning(f"[TCPServerData] Client {str(address)} has disconnected with message: `{repr(e)}`")
    finally:
        try:
            client.close()
        except Exception as e:
            logging.error(f"[TCPServerData] Failed to close connection with message: `{repr(e)}`")
    global n_connections_data
    n_connections_data.decrement()

def server_remote_modality(client: socket.socket, address):
    logging.debug("[TCPServerModality] Client " + str(address) + " has connected")
    try:
        data = client.recv(50)
        if data:
            message = data.decode()
            message = message.split(' ')
            response = RESPONSE_REJECT
            if message[1] == Data.MODE_MANUAL:
                if MySharedData.set_manual(message[0]):
                    response = RESPONSE_ACCEPT
            elif message[1] == Data.MODE_AUTOMATIC:
                if MySharedData.set_automatic(message[0]):
                    response = RESPONSE_ACCEPT
            if response == RESPONSE_ACCEPT:
                logging.debug(f"[TCPServerModality] Water-Channel-Controller - Sent new modality")
                MyController.send_modality()
            client.sendall(str.encode(response))
    except Exception as e:
        logging.warning(f"[TCPServerModality] Client {str(address)} has disconnected with message: `{repr(e)}`")
    finally:
        try:
            client.close()
        except Exception as e:
            logging.error(f"[TCPServerModality] Failed to close connection with message: `{repr(e)}`")
    global n_connections_modality
    n_connections_modality.decrement()

def server_remote_valve_level(client: socket.socket, address):
    logging.debug("[TCPServerValveLevel] Client " + str(address) + " has connected")
    try:
        data = client.recv(50)
        if data:
            message = data.decode()
            message = message.split(' ')
            response = RESPONSE_REJECT
            if MySharedData.is_modality_manual():
                if MySharedData.set_valve_percentage_addr(message[0], int(message[1])):
                    response = RESPONSE_ACCEPT
            if response == RESPONSE_ACCEPT:
                logging.debug(f"[TCPServerValveLevel] Water-Channel-Controller - Sent new valve level")
                MyController.send_valve_percentage()
            client.sendall(str.encode(response))
    except Exception as e:
        logging.warning(f"[TCPServerValveLevel] Client {str(address)} has disconnected with message: `{repr(e)}`")
    finally:
        try:
            client.close()
        except Exception as e:
            logging.error(f"[TCPServerValveLevel] Failed to close connection with message: `{repr(e)}`")
    global n_connections_valve_level
    n_connections_valve_level.decrement()

# Waits for new connections
def manage_new_connection_data(socket: socket.socket):
    global n_connections_data
    n_conns = n_connections_data.value()
    while True:
        client, address = socket.accept()
        if n_conns <= N_CONNS_LIMIT:
            threading.Thread(target = server_data, args = (client, address), daemon=True).start()
            n_conns = n_connections_data.increment()
        else:
            logging.warning(f"[ConnectionsManagerData] Too much connections open, max connections permitted are {N_CONNS_LIMIT}, refused connection with {address}")
            client.close()

# Waits for new connections
def manage_new_connection_modality(socket: socket.socket):
    global n_connections_modality
    n_conns = n_connections_modality.value()
    while True:
        client, address = socket.accept()
        if n_conns <= N_CONNS_LIMIT:
            threading.Thread(target = server_remote_modality, args = (client, address), daemon=True).start()
            n_conns = n_connections_modality.increment()
        else:
            logging.warning(f"[ConnectionsManagerModality] Too much connections open, max connections permitted are {N_CONNS_LIMIT}, refused connection with {address}")
            client.close()

# Waits for new connections
def manage_new_connection_valve_level(socket: socket.socket):
    global n_connections_valve_level
    n_conns = n_connections_valve_level.value()
    while True:
        client, address = socket.accept()
        if n_conns <= N_CONNS_LIMIT:
            threading.Thread(target = server_remote_valve_level, args = (client, address), daemon=True).start()
            n_conns = n_connections_valve_level.increment()
        else:
            logging.warning(f"[ConnectionsManagerValveLevel] Too much connections open, max connections permitted are {N_CONNS_LIMIT}, refused connection with {address}")
            client.close()

def start(host):
    try:
        # Create new server socket
        serverData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverData.bind((host, 57134))
        serverData.listen()

        # Create new server socket
        serverModality = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverModality.bind((host, 57150))
        serverModality.listen()

        # Create new server socket
        serverValveLevel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverValveLevel.bind((host, 57183))
        serverValveLevel.listen()

        # Create new threads to wait for connections
        threading.Thread(target = manage_new_connection_data, args = (serverData,), daemon=True).start()
        threading.Thread(target = manage_new_connection_modality, args = (serverModality,), daemon=True).start()
        threading.Thread(target = manage_new_connection_valve_level, args = (serverValveLevel,), daemon=True).start()
    except Exception as e:
        logging.error(f"[River-Monitoring-Dashboard] Failed to create server sockets with message: `{repr(e)}`")
