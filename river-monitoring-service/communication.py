import logging
import sys, time, threading
import monitor
from controller import MyController
from data import Data, MySharedData
from datetime import datetime
import dashboard

def on_monitor_message(client, userdata, msg):
    sampling_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    water_level = float(msg.payload.decode())
    logging.info(f"[Water-Level-Monitoring] Received water level {water_level}")

    old_state = MySharedData.get_state()
    old_vl = MySharedData.get_valve_level()
    old_T = MySharedData.get_period()
    MySharedData.set_data(water_level)

    state = MySharedData.get_state()
    valve_level = MySharedData.get_valve_level()
    MySharedData.set_dashboard_data(sampling_time, water_level, state, valve_level)
    if old_state != state:
        logging.info(f"[Policy] State changed to `{state}`")
        if old_vl != valve_level:
            if (MySharedData.is_modality_automatic()):
                MyController.send_valve_percentage()
        period = MySharedData.get_period()
        if old_T != period:
            monitor.publish(client, period)
            logging.info(f"[Water-Level-Monitoring] Sent new period `{period}`")

# This function should receive data periodically to avoid potential errors
def _check_data():
    valve_controller_mode = Data.MODE_AUTOMATIC
    disconnected = 1
    while True:
        read_data = False
        data = MyController.receive_data()
        if data is not None:
            if disconnected != 1:
                disconnected = 1
            if data != "":
                last_space_index = data.rfind(' ')
                if last_space_index != -1:
                    read_data = True
                    prefix = data[:last_space_index]
                    suffix = data[last_space_index + 1:len(data) - 2]
                    # To work correctly expects 3 data packets in this order:
                    if prefix == "local mode":
                        valve_controller_mode = suffix
                    elif prefix == "mode":
                        modality = MySharedData.get_modality()
                        if modality != suffix:
                            logging.info(f"[CheckDataDaemon] Sent modality `{modality}` because received `{suffix}`")
                            MyController.send_modality()
                    elif prefix == "valve percentage":
                        if valve_controller_mode == Data.MODE_AUTOMATIC:
                            valve_level = MySharedData.get_valve_level()
                            if str(valve_level) != suffix:
                                logging.info(f"[CheckDataDaemon] Sent valve percentage to `{valve_level}` because received `{suffix}`")
                                MyController.send_valve_percentage()
        else:
            time.sleep(disconnected)
            disconnected = max(disconnected + 1, 30)
        if not read_data:
            time.sleep(0.5)

def start(host):
    client = monitor.connect_mqtt(on_monitor_message)
    threading.Thread(target = _check_data, daemon=True).start()
    dashboard.start(host)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        sys.exit()
