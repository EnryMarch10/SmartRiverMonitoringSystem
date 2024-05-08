#ifndef __BUTTON_IMPL__
#define __BUTTON_IMPL__

#include "Button.h"

class ButtonImpl: public Button {

public:
    ButtonImpl(const int pin);
    bool isPressed(void);
    ~ButtonImpl(void) { }

private:
    int pin;

};

#endif
