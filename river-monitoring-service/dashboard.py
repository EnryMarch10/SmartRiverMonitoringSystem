import logging
import threading, time, socket
import atomic_counter
from data import MySharedData

N_CONNS_LIMIT = 5

n_connections_data = atomic_counter.AtomicCounter()
n_connections_modality = atomic_counter.AtomicCounter()

def server_data(client: socket.socket, address):
    logging.info("[TCPServerData] Client " + str(address) + " has connected")
    sent_sampling_time = ""
    sent_state = ""
    sent_valve_level = -1
    try:
        while True:
            sampling_time, water_level, state, valve_level = MySharedData.get_dashboard_data()
            if sent_sampling_time != sampling_time:
                client.sendall(str.encode(f"water_level {sampling_time} {water_level}"))
            if sent_state != state:
                client.sendall(str.encode(f"state {state}"))
            if sent_valve_level != valve_level:
                client.sendall(str.encode(f"valve_level {valve_level}"))
            time.sleep(0.5)
    except:
        logging.warning("[TCPServerData] Client " + str(address) + " has disconnected")
    finally:
        try:
            client.close()
        except Exception as e:
            logging.error(f"[TCPServerData] Failed to close connection with message: `{repr(e)}`")
    global n_connections_data
    n_connections_data.decrement()

def server_remote(client: socket.socket, address):
    logging.info("[TCPServerModality] Client " + str(address) + " has connected")
    try:
        while True:
            data = client.recv(50)
            if data:
                if data == "MANUAL":
                    message = "UNACCEPTED"
                    if MySharedData.set_manual(address):
                        message = "ACCEPTED"
                    client.sendall(str.encode(message))
                elif data == "AUTOMATIC":
                    MySharedData.set_automatic(address)
    except:
        logging.warning("[TCPServerModality] Client " + str(address) + " has disconnected")
    finally:
        try:
            client.close()
        except Exception as e:
            logging.error(f"[TCPServerModality] Failed to close connection with message: `{repr(e)}`")
    global n_connections_modality
    n_connections_modality.decrement()

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
    n_conns = n_connections_data.value()
    while True:
        client, address = socket.accept()
        if n_conns <= N_CONNS_LIMIT:
            threading.Thread(target = server_remote, args = (client, address), daemon=True).start()
            n_conns = n_connections_modality.increment()
        else:
            logging.warning(f"[ConnectionsManagerModality] Too much connections open, max connections permitted are {N_CONNS_LIMIT}, refused connection with {address}")
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

        # Create new threads to wait for connections
        threading.Thread(target = manage_new_connection_data, args = (serverData,), daemon=True).start()
        threading.Thread(target = manage_new_connection_modality, args = (serverModality,), daemon=True).start()

        logging.info(f"[River-Monitoring-Dashboard] Created servers correctly")
    except Exception as e:
        logging.error(f"[River-Monitoring-Dashboard] Failed to create server sockets with message: `{repr(e)}`")
