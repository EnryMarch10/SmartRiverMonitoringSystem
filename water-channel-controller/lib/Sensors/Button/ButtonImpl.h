#ifndef __BUTTON_IMPL__
#define __BUTTON_IMPL__

#include "Button.h"

class ButtonImpl: public Button {

public:
    ButtonImpl(const int pin);
    bool isPressed(void);
    void notifyInterrupt(const int pin);
    ~ButtonImpl(void) { }

private:
    int pin;
    long lastEventTime;

};

#endif
