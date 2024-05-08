#ifndef __LED__
#define __LED__

#include "Light.h"

class Led: public Light {

public:
    Led(const int pin);
    bool isOn(void);
    bool isOff(void);
    void switchOn(void);
    void switchOff(void);
    void toggle(void);
    ~Led(void) { }

private:
    void setHigh(void);
    void setLow(void);
    int pin;
    void (Led::*doToggle)(void);

};

#endif
