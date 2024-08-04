#include "Led.h"

Led::Led(const int pin) {
    this->pin = pin;
    pinMode(this->pin, OUTPUT);
    setLow();
}

void Led::setHigh(void) {
    digitalWrite(pin, HIGH);
    doToggle = &Led::setLow;
}

void Led::setLow(void) {
    digitalWrite(pin, LOW);
    doToggle = &Led::setHigh;
}

bool Led::isOn(void) {
    return doToggle != &Led::setHigh;
}

bool Led::isOff(void) {
    return !isOn();
}

void Led::switchOn(void) {
    if (!isOn()) {
        setHigh();
    }
}

void Led::switchOff(void) {
    if (isOn()) {
        setLow();
    }
}

void Led::toggle(void) {
    (*this.*doToggle)();
}
