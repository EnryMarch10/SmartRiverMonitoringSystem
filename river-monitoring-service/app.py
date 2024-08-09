import sys
import threading
import policy, monitor, controller

# TODO: check if not correct to put it there when the lib isn't installed, or it can't be done
# from paho.mqtt import client as mqtt_client

def on_monitor_message(client, userdata, msg):
    water_level = float(msg.payload.decode())
    # Send new water level to River-Monitoring-Dashboard
    print(f"[POLICY] Received water level {water_level}")

    old_state = policy.state
    old_vl = policy.valve_level
    old_T = policy.period
    policy.set_data(water_level)

    if (policy.state != old_state):
        print(f"[POLICY] State changed to {policy.state}")
        # Send new state to River-Monitoring-Dashboard
        if (old_vl != policy.valve_level):
            if (policy.modality != policy.MODE_REMOTE_MANUAL): # MODALITY == AUTOMATIC
                # Send new VL to Water-Channel-Controller if not in manual mode
                policy.send_valve_percentage(arduino)
                # raise NotImplementedError()
        if (old_T != policy.period):
            # Send new T to Water-Level-Monitoring
            monitor.publish(client, policy.period)
            print(f"[POLICY] Sent new period `{policy.period}` ms to Water-Level-Monitoring")
    # print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')

if __name__ == '__main__':
    arduino = controller.Controller()
    client = monitor.connect_mqtt(on_monitor_message)
    threading.Thread(target = policy.check_data, args = (arduino,), daemon=True).start()
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        sys.exit()
