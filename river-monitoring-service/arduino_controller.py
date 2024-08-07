import random
import string
import sys
import threading
import time
import check_library

check_library.check_or_install_library("pyserial")

import serial
import ports_finder

COM_PORT_DESCRIPTION = "Arduino Uno"

def _check_presence(arduino_port: str, event: threading.Event, interval=0.1):
    message_not_found = False
    message_disconnected = False
    previous_ports = []
    while not event.is_set():
        ports = ports_finder.print_com_ports(COM_PORT_DESCRIPTION)

        if message_disconnected is False and arduino_port not in ports:
            print(f"[ArduinoUnoControllerDaemon] `{COM_PORT_DESCRIPTION}` disconnected from `{arduino_port}` connected port!", file=sys.stderr)
            message_disconnected = True

        if len(ports) > 0:
            if message_not_found:
                message_not_found = False
            if ports != previous_ports:
                if len(ports) == 1:
                    print(f"[ArduinoUnoControllerDaemon] `{COM_PORT_DESCRIPTION}` connected to `{ports[0]}` port")
                else:
                    print(f"[ArduinoUnoControllerDaemon] `{COM_PORT_DESCRIPTION}` connected to `{", ".join(ports)}` ports")
                previous_ports = ports
        else:
            if message_not_found is False:
                print(f"[ArduinoUnoControllerDaemon] `{COM_PORT_DESCRIPTION}` disconnected, not found in any port!")
                message_not_found = True
                previous_ports.clear()
        time.sleep(interval)

class ArduinoController:
    def __init__(self, port="", baud_rate=9600) -> None:
        self._connected = False
        self.try_connect(port, baud_rate)

    def try_connect(self, port="", baud_rate=9600) -> bool:
        if port == "":
            ports = ports_finder.print_com_ports(COM_PORT_DESCRIPTION)
            if len(ports) > 0:
                port = ports[0]
            else:
                print(f"[ArduinoUnoController] `{COM_PORT_DESCRIPTION}` not found in COM ports descriptions", file=sys.stderr)
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
            print(f"[ArduinoUnoController] Connected successfully at `{port}` port")
            return True
        except Exception as e:
            print(f"[ArduinoUnoController] Failed to connect at `{port}` port with message: `{repr(e)}`", file=sys.stderr)
            self._connected = False
            return False

    def send_data(self, message) -> bool:
        try:
            self._arduino_uno.write(
                str.encode(f"{str.encode("".join(random.choice(string.ascii_letters + string.digits) for _ in range(8)),
                                         encoding='ascii')} {str(message)}\n", encoding='ascii'))
            print(f"[ArduinoUnoController] Message sent: `{message}`")
            return True
        except Exception as e:
            print(f"[ArduinoUnoController] Failed to send message with message: `{repr(e)}`", file=sys.stderr)
            return False

    def receive_data(self) -> str | None:
        try:
            return self._arduino_uno.readline().decode(encoding='ascii')
        except Exception as e:
            print(f"[ArduinoUnoController] Failed to receive message with message: `{repr(e)}`", file=sys.stderr)
            return None

    def close_connection(self) -> bool:
        try:
            if self._connected:
                self._stop_event.set()
                self._port_controller.join()
                self._connected = False
                self._arduino_uno.close()
            return True
        except Exception as e:
            print(f"[ArduinoUnoController] Failed to close connection with message: `{repr(e)}`", file=sys.stderr)
            return False