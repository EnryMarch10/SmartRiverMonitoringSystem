#include "config.h"
#include "Led.h"
#include "SonarImpl.h"

extern Led ledGreen;
extern Led ledRed;
extern SonarImpl sonar;

void setup() {
    Serial.begin(BAUD_RATE);
    ledRed.switchOn();
}

void loop() {
    delay(2000);
    ledGreen.toggle();
    Serial.println("Distance is " + String(sonar.getDistance()) + " cm");
}
