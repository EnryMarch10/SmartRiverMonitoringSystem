import random
import string
import threading
import time
import utils.check_library as check_library
import logging

check_library.check_or_install_library("pyserial")

import serial
import utils.ports_finder as ports_finder

COM_PORT_DESCRIPTION = "Arduino Uno"

def _check_presence(arduino_port: str, event: threading.Event, interval=0.1):
    message_not_found = False
    message_disconnected = False
    previous_ports = []
    while not event.is_set():
        ports = ports_finder.print_com_ports(COM_PORT_DESCRIPTION)

        if message_disconnected is False and arduino_port not in ports:
            logging.info(f"[ArduinoUnoControllerDaemon] `{COM_PORT_DESCRIPTION}` disconnected from `{arduino_port}` connected port!")
            message_disconnected = True

        if len(ports) > 0:
            if message_not_found:
                message_not_found = False
            if ports != previous_ports:
                if len(ports) == 1:
                    logging.info(f"[ArduinoUnoControllerDaemon] `{COM_PORT_DESCRIPTION}` connected to `{ports[0]}` port")
                else:
                    logging.info(f"[ArduinoUnoControllerDaemon] `{COM_PORT_DESCRIPTION}` connected to `{", ".join(ports)}` ports")
                previous_ports = ports
        else:
            if message_not_found is False:
                logging.info(f"[ArduinoUnoControllerDaemon] `{COM_PORT_DESCRIPTION}` disconnected, not found in any port!")
                message_not_found = True
                previous_ports.clear()
        time.sleep(interval)

class ArduinoController:
    def __init__(self, port="", baud_rate=9600) -> None:
        self._connected = False
        self.try_connect(port, baud_rate)
    
    def is_connected(self):
        return self._arduino_uno.is_open

    def try_connect(self, port="", baud_rate=9600) -> bool:
        if not port:
            ports = ports_finder.print_com_ports(COM_PORT_DESCRIPTION)
            if len(ports) > 0:
                port = ports[0]
            else:
                logging.warning(f"[ArduinoUnoController] `{COM_PORT_DESCRIPTION}` not found in COM ports descriptions")
                return False
        try:
            if self._connected:
                self._stop_event.set()
                self._port_controller.join()
            self._arduino_uno = serial.Serial(port, baudrate=baud_rate, timeout=1.0)
            self._arduino_port = port
            self._stop_event = threading.Event()
            self._port_controller = threading.Thread(target=_check_presence, args=(self._arduino_port, self._stop_event, 0.5), daemon=True)
            self._port_controller.start()
            self._connected = True
            logging.info(f"[ArduinoUnoController] Connected successfully at `{port}` port")
            time.sleep(1)
            return True
        except Exception as e:
            logging.error(f"[ArduinoUnoController] Failed to connect at `{port}` port with message: `{repr(e)}`")
            self._connected = False
            return False

    def try_send_data(self, message) -> bool:
        result = False
        try:
            self._arduino_uno.write(
                str.encode(f"{str.encode("".join(random.choice(string.ascii_letters + string.digits) for _ in range(8)),
                                         encoding='ascii')} {str(message)}\n", encoding='ascii'))
            result = True
        except Exception as e:
            logging.error(f"[ArduinoUnoController] Failed to send message with message: `{repr(e)}`")
        finally:
            return result

    def send_data(self, message) -> bool:
        data = self.try_send_data(message)
        if not data:
            if self.try_connect():
                return self.try_send_data(message)
        return data

    def try_receive_data(self) -> str | None:
        data = ""
        try:
            if self._arduino_uno.in_waiting > 0:
                data = self._arduino_uno.readline().decode(encoding='ascii')
        except Exception as e:
            logging.error(f"[ArduinoUnoController] Failed to receive message with message: `{repr(e)}`")
            data = None
        finally:
            return data

    def receive_data(self) -> str | None:
        data = self.try_receive_data()
        if data is None:
            if self.try_connect():
                return self.try_receive_data()
        return data

    def close_connection(self) -> bool:
        try:
            if self._connected:
                self._stop_event.set()
                self._port_controller.join()
                self._connected = False
                self._arduino_uno.close()
            return True
        except Exception as e:
            logging.error(f"[ArduinoUnoController] Failed to close connection with message: `{repr(e)}`")
            return False
