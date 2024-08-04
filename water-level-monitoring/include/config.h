/**
 * General configuration file that defines run options and pins of the sensors in current circuit.
*/
#ifndef __CONFIG__
#define __CONFIG__

#include "utils.h"
#include <PubSubClient.h>

// PINS configuration

#define PIN_LED_GREEN 10
#define PIN_LED_RED 9

#define PIN_SONAR_TRIG 18
#define PIN_SONAR_ECHO 17

#define DEF_T 10000 // ms

/**
 * Initializes the sensors/actuators using the configured pins.
*/
void init_config(const char *wifi_ssid, const char *wifi_password, MQTT_CALLBACK_SIGNATURE);

void mqtt_connect(void);

#endif
