#include "Potentiometer.h"

Potentiometer::Potentiometer(int pin) {
    this->pin = pin;
}

void Potentiometer::sync(void) {
    value = analogRead(pin);
    updateSyncTime(millis());
}

float Potentiometer::getValue(void) {
    return value / 1023.0;
}

void Potentiometer::updateSyncTime(long time) {
	lastTimeSync = time;
}

long Potentiometer::getLastSyncTime(void) {
	return lastTimeSync;
}
