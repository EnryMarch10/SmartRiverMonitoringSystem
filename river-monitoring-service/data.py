import threading

class Data():
    _instance = None

    _lock_singleton = threading.Lock()
    _lock_state = threading.Lock()
    _lock_valve_level = threading.Lock()
    _lock_period = threading.Lock()
    _lock_modality = threading.Lock()

    # System modalities
    MODE_AUTOMATIC = "AUTOMATIC"
    MODE_MANUAL = "MANUAL"
    MODE_REMOTE_MANUAL = "REMOTE_MANUAL"

    # Water levels (just for testing, no unit of measurement)
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

    def __new__(self):
        if self._instance is None: 
            with self._lock_singleton:
                if not self._instance:
                    self._instance = super().__new__(self)
        return self._instance

    def __init__(self) -> None:
        self._state = Data.STATE_NORMAL
        self._valve_level = Data.VALVE_ONE_QUARTER
        self._period = Data.T1
        self._remote_mode = Data.MODE_AUTOMATIC
        self._remote_address = ""

    def get_state(self):
        with self._lock_state:
            return self._state
    
    def get_valve_level(self):
        with self._lock_valve_level:
            return self._valve_level
    
    def get_period(self):
        with self._lock_period:
            return self._period
    
    def get_modality(self):
        with self._lock_modality:
            return self._remote_mode
    
    def is_modality_automatic(self):
        with self._lock_modality:
            return self._remote_mode == Data.MODE_AUTOMATIC
    
    def is_modality_manual(self):
        with self._lock_modality:
            return self._remote_mode == Data.MODE_REMOTE_MANUAL
    
    def set_state(self, state: str):
        with self._lock_state:
            self._state = state
    
    def set_valve_level(self, valve_level):
        with self._lock_valve_level:
            self._valve_level = valve_level
    
    def set_period(self, period):
        with self._lock_period:
            self._period = period

    def set_automatic(self):
        with self._lock_modality:
            if self._remote_mode == Data.MODE_AUTOMATIC:
                return False
            self._remote_mode = Data.MODE_AUTOMATIC
            self._remote_address = ""
        return True

    def set_manual(self, address) -> bool:
        with self._lock_modality:
            if self._remote_mode == Data.MODE_REMOTE_MANUAL:
                return False
            if self._remote_address == address:
                return True
            self._remote_mode = Data.MODE_REMOTE_MANUAL
            self._remote_address = address
        return True

    def set_data(self, water_level: float):
        if (water_level < Data.WL1):
            self.set_state(Data.STATE_ALARM_TOO_LOW)
            self.set_valve_level(Data.VALVE_CLOSE)
            self.set_period(Data.T1)
        elif (water_level > Data.WL1 and water_level <= Data.WL2):
            self.set_state(Data.STATE_NORMAL)
            self.set_valve_level(Data.VALVE_ONE_QUARTER)
            self.set_period(Data.T1)
        elif (water_level > Data.WL2 and water_level <= Data.WL3):
            self.set_state(Data.STATE_PRE_ALARM_TOO_HIGH)
            self.set_valve_level(Data.VALVE_ONE_QUARTER)
            self.set_period(Data.T2)
        elif (water_level > Data.WL3 and water_level <= Data.WL4):
            self.set_state(Data.STATE_ALARM_TOO_HIGH)
            self.set_valve_level(Data.VALVE_HALF)
            self.set_period(Data.T2)
        else: # elif (water_level > WL4):
            self.set_state(Data.STATE_ALARM_TOO_HIGH_CRITIC)
            self.set_valve_level(Data.VALVE_OPEN)
            self.set_period(Data.T2)

MySharedData = Data()
