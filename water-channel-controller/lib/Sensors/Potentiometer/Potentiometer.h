#ifndef __POTENTIOMETER__
#define __POTENTIOMETER__

#include "utils.h"

class Potentiometer {

public:
    Potentiometer(const int pin);
    Potentiometer(const int pin, const int min_value, const int max_value);
    int getValue(void);

private:
    int pin;
    float value;

    float min_value;
    float max_value;
};

#endif
