#include "config.h"

#include "ButtonImpl.h"
#include "ServoMotorImpl.h"
#include "LcdI2C.h"
#include "Potentiometer.h"

extern ButtonImpl button;
extern ServoMotorImpl servoMotor;
extern LcdI2C lcd;
extern Potentiometer potentiometer;

void setup() {
    Serial.begin(BAUD_RATE);
    lcd.init();
    servoMotor.on();
}

void loop() {
    servoMotor.open();
    delay(500);
    Serial.println("Button is pressed = " + String(button.isPressed()));
    potentiometer.sync();
    Serial.println("Potentiometer value is " + String(potentiometer.getValue()));
    lcd.on();
    lcd.write("Hello");
    delay(1000);
    lcd.off();
    servoMotor.close();
    Serial.println("Button is pressed = " + String(button.isPressed()));
    potentiometer.sync();
    Serial.println("Potentiometer value is " + String(potentiometer.getValue()));
    delay(500);
}
    