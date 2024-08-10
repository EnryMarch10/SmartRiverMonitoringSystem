import utils.check_library as check_library

check_library.check_or_install_library("pyserial")

import serial.tools.list_ports as ports

def print_com_ports(description):
    found_ports = []
    for port in list(ports.comports()):
        if description in port.description:
            found_ports.append(port.name)
    return found_ports
