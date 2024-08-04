#include "ButtonImpl.h"

#define DEBOUNCING_TIME 20

ButtonImpl::ButtonImpl(const int pin) : Button(pin) {
    this->pin = pin;
    pinMode(pin, INPUT);
    lastEventTime = millis();
}

bool ButtonImpl::isPressed(void) {
    return digitalRead(pin) == HIGH;
}

void ButtonImpl::notifyInterrupt(int pin) {
    long curr = millis();
    if (curr - lastEventTime > DEBOUNCING_TIME) {
        lastEventTime = curr;
        Event *ev;
        if (isPressed()) {
            ev = new ButtonPressed(this);
        } else {
            ev = new ButtonReleased(this);
        }
        generateEvent(ev);
    }
}
