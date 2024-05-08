# Assignment \#3 - Smart River-Monitoring System

Third assignment on a system based on Arduino UNO R3, ESP32-S3 and two desktop applications of
[Embedded Systems and IoT - a.y. 2023-2024](https://www.unibo.it/en/teaching/course-unit-catalogue/course-unit/2023/400396)
([Computer Science and Engineering](https://corsi.unibo.it/1cycle/ComputerScienceEngineering)).

## Author

[@EnryMarch10](https://github.com/EnryMarch10)

## Behavior

We want to realize an IoT system implementing a simplified version of a smart river monitoring system,
as a system monitoring the water level of rivers and controlling related water channels.

![system schema](img/assignment-3%20result.jpg)

The system is composed of 4 subsystems:
- **water-level-monitoring** subsystem (ESP32):
    - embedded system to monitor the water level of a river;
    - it interacts with the *river-monitoring-service* subsystem (preferably via MQTT but HTTP can be used as a second option);
- **water-channel-controller** subsystem (Arduino):
    - embedded system controlling the gate/valve of a water channel;
    - it interacts via serial line with the *river-monitoring-service* subsystem;
- **river-monitoring-service** subsystem (backend - running on a PC server):
    - service functioning as the main unit governing the management of the Smart River-Monitoring System;
    - it interacts through the serial line with the *water-channel-controller* subsystem;
    - it interacts via MQTT with the *water-level-monitoring* subsystem;
    - it interacts via HTTP with the *river-monitoring-dashboard* subsystem;
- **river-monitoring-dashboard** subsystem (frontend/web app - running on the PC):
    - frontend to visualize and track the state of the *river-monitoring-service* subsystem;
    - it interacts with the *river-monitoring-service* subsystem via HTTP.

Hardware components:
- **water-level-monitoring** subsystem:
    - SoC ESP32 board including:
        - 1 green led;
        - 1 red led;
        - 1 sonar;
- **water-channel-controller** subsystem:
    - Micro controller Arduino UNO board including:
        - 1 servo motor;
        - 1 button;
        - 1 potentiometer;
        - 1 LCD display.

### General Behavior

The Smart River-Monitoring System is meant to monitor the water level of a river and, depending on the level,
controlling a valve to distribute the water to some channels.

### Detailed Behavior

About the **water-level-monitoring** subsystem:
- this subsystem is responsible for continuously monitoring the level of the water, by means of the sonar;
- the water level is sampled and sent to the *river-monitoring-service* subsystem with some frequency F:
    - this frequency depends on the state of the system and is established by the *river-monitoring-service* subsystem (see later);
- when the system is working correctly (network and sending data ok) the green led is on and the red is off; otherwise,
  in case of network problems, the red led should be on and the green led off.

About the **water-channel-controller** subsystem:
- this subsystem is responsible for controlling the valve establishing how much water should flow to the channels,
  and this is determined by the valve opening level: from 0% = full closed (no water flows from river to channels),
  up to 100% = full open;
    - the valve is implemented by the servo motor: angle 0° corresponds to valve opening level 0%,
      angle 180° corresponds to valve opening level 100%;
- the valve opening level depends on the state of the system, established by the *river-monitoring-service* subsystem (see later);
- this subsystem provides also a button to enable a manual control modality:
    - when the button is pressed, the controller enters in manual mode, so that the valve opening level can be manually controlled
      by operators using a potentiometer: to exit from the manual mode, the button should be pressed again;
- this subsystem is also equipped with an LCD display reporting the current valve opening level and current modality
  (AUTOMATIC or MANUAL).

About the **river-monitoring-service** subsystem:
- this subsystem decides the overall policy and behavior of the river monitoring system, depending on the water level as measured
  by the *water-level-monitoring* subsystem, policy:
- when the water level is in the range [WL1, WL2], then the system is considered in a NORMAL state. In the NORMAL state:
    - the frequency to be used for monitoring the water level is F1;
    - the valve opening level should be 25%;
- when the water level is < WL1, the system is in an ALARM-TOO-LOW state: 
    - in this state, the valve opening level should be 0%;
- when the water level is > WL2,  there are three further cases:
    - WL2 < water-level <= WL3 → the system is in a PRE-ALARM-TOO-HIGH state:
        - In this state, the frequency to be used for monitoring the water level should be increased to F2 (where F2 > F1);
    - WL3 < water-level <= WL4 → ALARM-TOO-HIGH state:
        - In this state the frequency is still F2, but the valve opening level must be 50%;
    - water-level > WL4 → ALARM-TOO-HIGH-CRITIC state:
        - In this state, the frequency is still F2, but the valve opening level should be 100%.

About the **river-monitoring-dashboard** subsystem:
- this subsystem has two main responsibilities:
    - to visualize the state of the River Monitoring system. In particular:
        - the graph of water level trend, considering a certain temporal window (the last N minutes);
        - the state of the system:
            - NORMAL, ALARM-TOO-LOW, PRE-ALARM-TOO-HIGH, ALARM-TOO-HIGH, ALARM-TOO-HIGH-CRITIC;
        - the valve opening level;
    - to allow a user for controlling manually, from remote, the valve opening level.

### Assignment Further Requirements

Design and develop a prototype of the Smart River-Monitoring system, considering as further requirements:

- **water-level-monitoring** subsystem:
    - Run on ESP32 or ESP8266;
    - Must use preferably MQTT to communicate with the *river-monitoring-service* subsystem;
- **water-channel-controller** subsystem:
    - Run on Arduino;
    - The control logic must be designed and implemented using finite state machines (synchronous or asynchronous);
    - Communicate with the River Monitoring Service via serial line;
- **river-monitoring-service** subsystem:
    - Run on a PC;
    - No specific constraints about the programming/sw technology to be used;
    - Use preferably MQTT to communicate with the *water-level-monitoring* subsystem;
- **river-monitoring-dashboard** subsystem:
    - Run on a PC;
    - No specific constraints on the technologies to be used;
    - Can be implemented as a web app running in a browser interacting via HTTP with the service or
      a PC app based on HTTP sockets.

## License

[MIT](https://choosealicense.com/licenses/mit/)
