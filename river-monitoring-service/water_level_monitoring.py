import sys, time, random, string
import check_library

check_library.check_or_install_library("paho-mqtt")

from paho.mqtt import client as mqtt_client

BROKER = "broker.emqx.io"
PORT = 8883
TOPIC_WATER_LEVEL = "SmartRiverMonitoringSystem/WaterLevelMonitoring/WaterLevel"
TOPIC_PERIOD = "SmartRiverMonitoringSystem/WaterLevelMonitoring/Period"
CLIENT_ID = f"RiverMonitoringService-{"".join(random.choices(string.hexdigits, k=8))}"
USERNAME = "SmartRiverMonitoringSystem"
PASSWORD = "GtYu673Rt"

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def __on_connect(client: mqtt_client.Client, userdata, flags, rc):
    if rc == 0 and client.is_connected():
        print(f"[MQTT] Connected successfully to broker `{BROKER}`")
        client.subscribe(TOPIC_WATER_LEVEL)
    else:
        print(f"[MQTT] Failed to connect to broker `{BROKER}`, return code `{rc}`", file=sys.stderr)

def __on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected from broker `{BROKER}` with result code: `{rc}`")
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        print(f"[MQTT] Reconnecting in `{reconnect_delay}` seconds...")
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            print(f"[MQTT] Reconnected with broker `{BROKER}` successfully!")
            return
        except Exception as err:
            print(f"[MQTT] `{err}`. Reconnect failed. Retrying...")

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    print(f"[MQTT] Reconnect failed after `{reconnect_count}` attempts. Exiting...", file=sys.stderr)

def connect_mqtt(on_message) -> mqtt_client.Client:
    client = mqtt_client.Client(client_id=CLIENT_ID)
    client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = __on_connect
    client.on_message = on_message
    try:
        client.connect(BROKER, PORT, keepalive=120)
    except:
        print(f"[MQTT] Failed to connect to broker `{BROKER}` on port `{PORT}`", file=sys.stderr)
    client.on_disconnect = __on_disconnect
    return client

def publish(client: mqtt_client.Client, msg: str) -> bool:
    if not client.is_connected():
        print("[MQTT] Publish: MQTT client is not connected!", file=sys.stderr)
        time.sleep(1)
        return False
    result = client.publish(TOPIC_PERIOD, msg)
    status = result[0]
    if status == 0:
        print(f"[MQTT] Send `{msg}` to topic `{TOPIC_PERIOD}`")
        return True
    print(f"[MQTT] Failed to send message to topic `{TOPIC_PERIOD}`", file=sys.stderr)
    return False
