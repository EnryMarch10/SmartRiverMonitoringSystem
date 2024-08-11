import logging
import threading

class Data():
    _lock_singleton = threading.Lock()
    _instance = None

    _lock_state = threading.Lock()
    _lock_valve_level = threading.Lock()
    _lock_period = threading.Lock()
    _lock_modality = threading.Lock()
    _lock_dashboard_data = threading.Lock()

    _lock_timer = threading.Lock()
    _timer = None
    MANUAL_TIMEOUT = 20 # s

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

    # I am applying a thread safe version of the Singleton programming pattern
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
        # The following two variables must be modified together (same lock)
        self._remote_mode = Data.MODE_AUTOMATIC
        self._remote_address = None
        # Following data are a sort of cache of what to send to the River Monitoring Dashboard (same lock).
        # It helps to keep data in a coherent state (they have a logic one with another).
        # This avoids strange state of data from dashboard.
        self._last_sampling_time = None
        self._last_water_level = None
        self._last_state = None
        self._last_valve_level = None
        self._last_modality = None
        self._last_address = None

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
    
    def get_modality_addr(self):
        with self._lock_modality:
            return (self._remote_mode, self._remote_address)

    def is_modality_automatic(self):
        with self._lock_modality:
            return self._remote_mode == Data.MODE_AUTOMATIC

    def is_modality_manual(self):
        with self._lock_modality:
            return self._remote_mode == Data.MODE_REMOTE_MANUAL

    def get_dashboard_data(self):
        with self._lock_dashboard_data:
            return (self._last_sampling_time, self._last_water_level, self._last_state,
                    self._last_valve_level, self._last_modality, self._last_address)

    def set_state(self, state: str):
        with self._lock_state:
            self._state = state

    def set_valve_percentage(self, valve_level):
        with self._lock_valve_level:
            self._valve_level = valve_level

    def set_valve_percentage_addr(self, address, valve_level) -> bool:
        with self._lock_modality:
            if self._remote_address != address:
                return False
            with self._lock_valve_level:
                self._valve_level = valve_level
        with self._lock_timer:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(Data.MANUAL_TIMEOUT, self.set_automatic, args=(address,))
            self._timer.start()
        logging.debug(f"[Data] Reset and started new MANUAL timer of {Data.MANUAL_TIMEOUT} s")
        return True

    def set_period(self, period):
        with self._lock_period:
            self._period = period

    def set_automatic(self, address):
        with self._lock_modality:
            if self._remote_mode == Data.MODE_AUTOMATIC or self._remote_address != address:
                return False
            self._remote_mode = Data.MODE_AUTOMATIC
            self._remote_address = None
        with self._lock_timer:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
        logging.info(f"[Data] Deleting timer because AUTOMATIC mode was triggered (by timer or user)")
        return True

    def set_manual(self, address) -> bool:
        with self._lock_modality:
            if self._remote_mode == Data.MODE_REMOTE_MANUAL:
                return False
            if self._remote_address == address:
                return True
            self._remote_mode = Data.MODE_REMOTE_MANUAL
            self._remote_address = address
        with self._lock_timer:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(Data.MANUAL_TIMEOUT, self.set_automatic, args=(address,))
            self._timer.start()
        logging.debug(f"[Data] Started new MANUAL timer of {Data.MANUAL_TIMEOUT} s")
        return True

    def set_dashboard_data(self, sampling_time, water_level, state, valve_level, modality, address):
        with self._lock_dashboard_data:
            self._last_sampling_time = sampling_time
            self._last_water_level = water_level
            self._last_state = state
            self._last_valve_level = valve_level
            self._last_modality = modality
            self._last_address = address

    # This function should is called from a single thread, to make things work correctly.
    # Not sure about this, but I think that if this function is called by more threads
    # a lock to make the changes to all variables to be atomic should be created.
    # When new water level is read this function is called.
    def set_data(self, water_level: float):
        is_automatic = self.is_modality_automatic()
        if (water_level < Data.WL1):
            self.set_state(Data.STATE_ALARM_TOO_LOW)
            if is_automatic:
                self.set_valve_percentage(Data.VALVE_CLOSE)
            self.set_period(Data.T1)
        elif (water_level > Data.WL1 and water_level <= Data.WL2):
            self.set_state(Data.STATE_NORMAL)
            if is_automatic:
                self.set_valve_percentage(Data.VALVE_ONE_QUARTER)
            self.set_period(Data.T1)
        elif (water_level > Data.WL2 and water_level <= Data.WL3):
            self.set_state(Data.STATE_PRE_ALARM_TOO_HIGH)
            if is_automatic:
                self.set_valve_percentage(Data.VALVE_ONE_QUARTER)
            self.set_period(Data.T2)
        elif (water_level > Data.WL3 and water_level <= Data.WL4):
            self.set_state(Data.STATE_ALARM_TOO_HIGH)
            if is_automatic:
                self.set_valve_percentage(Data.VALVE_HALF)
            self.set_period(Data.T2)
        else: # elif (water_level > WL4):
            self.set_state(Data.STATE_ALARM_TOO_HIGH_CRITIC)
            if is_automatic:
                self.set_valve_percentage(Data.VALVE_OPEN)
            self.set_period(Data.T2)

MySharedData = Data()
