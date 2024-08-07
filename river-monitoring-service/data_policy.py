# System modalities
MODE_AUTOMATIC = "AUTOMATIC"
MODE_MANUAL = "MANUAL"

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
