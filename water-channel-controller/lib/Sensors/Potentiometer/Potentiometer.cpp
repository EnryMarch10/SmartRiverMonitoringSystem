#include "Potentiometer.h"

#define MIN_VALUE 0
#define MAX_VALUE 1023

Potentiometer::Potentiometer(const int pin) {
    this->pin = pin;
}

Potentiometer::Potentiometer(const int pin, const int min_value, const int max_value) {
    this->pin = pin;
    this->min_value = min_value;
    this->max_value = max_value;
}

int Potentiometer::getValue(void) {
    return map(analogRead(pin), MIN_VALUE, MAX_VALUE, min_value, max_value);
}
