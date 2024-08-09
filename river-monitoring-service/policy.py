import threading
import time
import controller

# System modalities
MODE_AUTOMATIC = "AUTOMATIC"
MODE_MANUAL = "MANUAL"
MODE_REMOTE_MANUAL = "REMOTE_MANUAL"

# Water levels (just for testing no unit of measurement)
WL1 = 5
WL2 = 10
WL3 = 15
WL4 = 20

# System states
STATE_ALARM_TOO_LOW = "ALARM-TOO-LOW"
STATE_NORMAL = "NORMAL"
STATE_PRE_ALARM_TOO_HIGH = "PRE-ALARM-TOO-HIGH"
STATE_ALARM_TOO_HIGH = "ALARM-TOO-HIGH"
STATE_ALARM_TOO_HIGH_CRITIC = "ALARM-TOO-HIGH-CRITIC"

# Valve levels (in %)
VALVE_CLOSE = 0
VALVE_ONE_QUARTER = 25
VALVE_HALF = 50
VALVE_OPEN = 100

# Water level sampling periods (in ms)
T1 = 10000
T2 = 2000

valve_controller_mode = MODE_AUTOMATIC

modality = MODE_AUTOMATIC

state = STATE_NORMAL
valve_level = VALVE_ONE_QUARTER
period = T1

def set_data(water_level: float):
    global state, valve_level, period
    # System POLICY
    if (water_level < WL1):
        state = STATE_ALARM_TOO_LOW
        valve_level = VALVE_CLOSE
        period = T1
    elif (water_level > WL1 and water_level <= WL2):
        state = STATE_NORMAL
        valve_level = VALVE_ONE_QUARTER
        period = T1
    elif (water_level > WL2 and water_level <= WL3):
        state = STATE_PRE_ALARM_TOO_HIGH
        valve_level = VALVE_ONE_QUARTER
        period = T2
    elif (water_level > WL3 and water_level <= WL4):
        state = STATE_ALARM_TOO_HIGH
        valve_level = VALVE_HALF
        period = T2
    else: # elif (water_level > WL4):
        state = STATE_ALARM_TOO_HIGH_CRITIC
        valve_level = VALVE_OPEN
        period = T2

lock_read = threading.Lock()
lock_percentage = threading.Lock()
lock_modality = threading.Lock()

def receive_data(controller : controller.Controller) -> str | None:
    global lock_read
    with lock_read:
        return controller.receive_data()

def send_valve_percentage(controller : controller.Controller) -> bool:
    global lock_percentage, valve_level
    with lock_percentage:
        result = controller.send_data(f"set valve percentage {valve_level}")
    if result:
        print(f"[POLICY] Sent new valve percentage `{valve_level}` % to Water-Channel-Controller")
    else:
        print(f"[POLICY] Failed to sent new valve percentage `{valve_level}` % to Water-Channel-Controller")
    return result

def send_modality(controller : controller.Controller) -> bool:
    global lock_modality, modality
    with lock_modality:
        result = controller.send_data(f"set mode {modality}")
    if result:
        print(f"[POLICY] Sent new modality `{modality}` to Water-Channel-Controller")
    else:
        print(f"[POLICY] Failed to sent new modality `{modality}` to Water-Channel-Controller")
    return result

# This function should be called periodically
def check_data(controller: controller.Controller):
    global valve_controller_mode, modality, valve_level
    disconnected = 1
    while True:
        read_data = False
        data = receive_data(controller)
        if data is not None:
            if disconnected != 1:
                disconnected = 1
            if data != "":
                last_space_index = data.rfind(' ')
                if last_space_index != -1:
                    read_data = True
                    prefix = data[:last_space_index]
                    suffix = data[last_space_index + 1:len(data) - 2]
                    if prefix == "local mode":
                        valve_controller_mode = suffix
                    elif prefix == "mode":
                        if valve_controller_mode == MODE_AUTOMATIC:
                            if modality != suffix:
                                send_modality(controller)
                    elif prefix == "valve percentage":
                        if valve_controller_mode == MODE_AUTOMATIC:
                            if valve_level != suffix:
                                send_valve_percentage(controller)
        else:
            time.sleep(disconnected)
            disconnected = max(disconnected + 1, 30)
        if not read_data:
            time.sleep(0.5)
            
