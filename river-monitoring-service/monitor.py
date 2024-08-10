import time, random, string
import utils.check_library as check_library
import logging

check_library.check_or_install_library("paho-mqtt")

from paho.mqtt import client as mqtt_client

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC_WATER_LEVEL = "SmartRiverMonitoringSystem/WaterLevelMonitoring/WaterLevel"
TOPIC_PERIOD = "SmartRiverMonitoringSystem/WaterLevelMonitoring/Period"
CLIENT_ID = f"RiverMonitoringService-{"".join(random.choices(string.hexdigits, k=8))}"
# USERNAME = "SmartRiverMonitoringSystem"
# PASSWORD = "GtYu673Rt"

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def __on_connect(client: mqtt_client.Client, userdata, flags, rc, properties=None):
    if rc == 0 and client.is_connected():
        logging.info(f"[MQTT] Connected successfully to broker `{BROKER}`")
        client.subscribe(TOPIC_WATER_LEVEL)
    else:
        logging.error(f"[MQTT] Failed to connect to broker `{BROKER}`, return code `{rc}`")

def __on_disconnect(client : mqtt_client.Client, userdata, rc, properties=None):
    logging.error(f"[MQTT] Disconnected from broker `{BROKER}` with result code: `{mqtt_client.error_string(rc)}`")
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info(f"[MQTT] Reconnecting in `{reconnect_delay}` seconds...")
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info(f"[MQTT] Reconnected with broker `{BROKER}` successfully!")
            return
        except Exception as err:
            logging.info(f"[MQTT] `{err}`. Reconnect failed. Retrying...")

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.error(f"[MQTT] Reconnect failed after `{reconnect_count}` attempts. Exiting...")

def connect_mqtt(on_message) -> mqtt_client.Client:
    client = mqtt_client.Client(client_id=CLIENT_ID, protocol=mqtt_client.MQTTv5)
    # client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
    # client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = __on_connect
    client.on_message = on_message
    try:
        client.connect(BROKER, PORT, keepalive=120)
    except Exception as e:
        logging.error(f"[MQTT] Failed to connect to broker `{BROKER}` on port `{PORT}` with message: `{repr(e)}`")
    client.on_disconnect = __on_disconnect
    return client

def publish(client: mqtt_client.Client, msg: str) -> bool:
    if not client.is_connected():
        logging.error("[MQTT] Publish: MQTT client is not connected!")
        time.sleep(1)
        return False
    result = client.publish(TOPIC_PERIOD, msg)
    status = result[0]
    if status == 0:
        logging.info(f"[MQTT] Send `{msg}` to topic `{TOPIC_PERIOD}`")
        return True
    logging.error(f"[MQTT] Failed to send message to topic `{TOPIC_PERIOD}`")
    return False
