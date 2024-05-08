#ifndef __BUTTON__
#define __BUTTON__

#include "utils.h"

class Button {

public:
    virtual bool isPressed(void) = 0;
    virtual ~Button(void) { }

};

#endif
