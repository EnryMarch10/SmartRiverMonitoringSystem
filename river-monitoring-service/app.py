import sys
import data_policy, water_level_monitoring, arduino_controller

# TODO: check if not correct to put it there when the lib isn't installed, or it can't be done
# from paho.mqtt import client as mqtt_client

def on_message(client, userdata, msg):
    water_level = float(msg.payload.decode())
    # Send new water level to River-Monitoring-Dashboard

    old_state = data_policy.state
    old_vl = data_policy.valve_level
    old_f = data_policy.period
    data_policy.set_data(water_level)

    if (data_policy.state != old_state):
        print(f"[POLICY] State changed to {data_policy.state}")
        # Send new state to River-Monitoring-Dashboard
        if (old_vl != data_policy.valve_level):
            if (data_policy.modality != data_policy.MODE_MANUAL): # MODALITY == AUTOMATIC
                # Send new VL to Water-Channel-Controller if not in manual mode
                newValveLevel = f"set valve percentage {data_policy.valve_level}"
                result = arduino.send_data(newValveLevel)
                if not result:
                    arduino.try_connect()
                    result = arduino.send_data(newValveLevel)
                if result:
                    print(f"[POLICY] Sent new valve percentage `{data_policy.valve_level}` % to Water-Channel-Controller")
                # raise NotImplementedError()
        if (old_f != data_policy.period):
            # Send new T to Water-Level-Monitoring
            water_level_monitoring.publish(client, data_policy.period)
            print(f"[POLICY] Sent new period `{data_policy.period}` ms to Water-Level-Monitoring")
    # print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')

if __name__ == '__main__':
    arduino = arduino_controller.ArduinoController()
    client = water_level_monitoring.connect_mqtt(on_message)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        sys.exit()
