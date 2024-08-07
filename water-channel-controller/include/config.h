/**
 * General configuration file that defines run options and pins of the sensors in current circuit.
*/
#ifndef __CONFIG__
#define __CONFIG__

#include "utils.h"
#include "Serial/Console.h"

// PINS configuration
#define PIN_POTENTIOMETER A0
#define PIN_BUTTON 2
#define PIN_SERVO_MOTOR 6
#define LCD_ADDRESS 0x3F

// States
#define AUTOMATIC F("AUTOMATIC")
#define MANUAL F("MANUAL")

/**
 * Initializes the sensors/actuators using the configured pins.
*/
void init_config(void);

#endif
