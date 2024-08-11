import logging
import threading
import arduino_controller
from data import MySharedData

class Controller:
    _instance = None

    _lock_singleton = threading.Lock()
    _lock_read = threading.Lock()
    _lock_write = threading.Lock()

    def __new__(self):
        if self._instance is None: 
            with self._lock_singleton:
                if not self._instance:
                    self._instance = super().__new__(self)
        return self._instance

    def __init__(self, port="", baud_rate=9600) -> None:
        self._arduino = arduino_controller.ArduinoController(port, baud_rate)

    def receive_data(self) -> str | None:
        with self._lock_read:
            data = self._arduino.receive_data()
        if data is not None and data:
            logging.debug(f"[Controller] Water-Channel-Controller - Received message `{data[:-2]}`")
        return data

    def send_valve_percentage(self) -> bool:
        with self._lock_write:
            result = self._arduino.send_data(f"set valve percentage {MySharedData.get_valve_level()}")
        if result:
            logging.debug(f"[Controller] Water-Channel-Controller - Sent valve percentage `{MySharedData.get_valve_level()}`")
        else:
            logging.debug(f"[Controller] Water-Channel-Controller - Failed to sent valve percentage `{MySharedData.get_valve_level()}`")
        return result

    def send_modality(self) -> bool:
        with self._lock_write:
            result = self._arduino.send_data(f"set mode {MySharedData.get_modality()}")
        if result:
            logging.debug(f"[Controller] Water-Channel-Controller - Sent modality `{MySharedData.get_modality()}`")
        else:
            logging.debug(f"[Controller] Water-Channel-Controller - Failed to sent modality `{MySharedData.get_modality()}`")
        return result

MyController = Controller()
