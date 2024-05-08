#include "config.h"

#include "ButtonImpl.h"
#include "ServoMotorImpl.h"
#include "LcdI2C.h"
#include "Potentiometer.h"

ButtonImpl button = ButtonImpl(PIN_BUTTON);
ServoMotorImpl servoMotor = ServoMotorImpl(PIN_SERVO_MOTOR);
LcdI2C lcd = LcdI2C(LCD_ADDRESS);
Potentiometer potentiometer = Potentiometer(PIN_POTENTIOMETER);
