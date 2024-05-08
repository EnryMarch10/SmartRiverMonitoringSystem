#ifndef __LIGHT__
#define __LIGHT__

#include "utils.h"

class Light {

public:
    /**
     * Tells if led is on.
    */
    virtual bool isOn(void) = 0;
    /**
     * Tells if led is off.
    */
    virtual bool isOff(void) = 0;
    /**
     * Switches the led on.
    */
    virtual void switchOn(void) = 0;
    /**
     * Switches the led off.
    */
    virtual void switchOff(void) = 0;
    /**
     * Toggles the led:
     * - switches the led on if current state is off;
     * - switches the led off if current state is on.
    */
    virtual void toggle(void) = 0;
    virtual ~Light(void) { }

};

#endif
