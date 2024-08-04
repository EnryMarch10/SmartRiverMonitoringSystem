#ifndef __VALVE__
#define __VALVE__

#include "ServoMotorImpl.h"

#define VALVE_INIT_TIMEOUT 2000 // ms
#define VALVE_STEP_TIMEOUT 200 // ms

class Valve : public ServoMotor {

public:
    Valve(const int pin) : ServoMotor(pin) { }
    void init(void);
    /**
     * Retrieves the valve opening level in percentage.
     * Returns a percentage between MIN_PERCENTAGE and MAX_PERCENTAGE.
    */
    int readPositionPercentage(void);
    /**
     * Starts to place the valve at the specified percentage in atomic way.
    */
    void setPositionPercentage(const int percentage);
    ~Valve(void) { }

private:
    int percentage;

};

#endif
