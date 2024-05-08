#include "ButtonImpl.h"

ButtonImpl::ButtonImpl(const int pin)
{
    this->pin = pin;
    pinMode(pin, INPUT);     
} 

bool ButtonImpl::isPressed()
{
    return digitalRead(pin) == HIGH;
}
