#ifndef __SERVO_MOTOR_IMPL__
#define __SERVO_MOTOR_IMPL__

#include "ServoMotor.h"

class ServoMotorImpl: public ServoMotor {

public:
    ServoMotorImpl(const int pin) : ServoMotor(pin) { }
    void init(void);
    /**
     * Retrieves the angle of rotation in degrees 0 to 180.
     */
    int readPositionAngle(void);
    /**
     * Accepts the angle of rotation in degrees 0 to 180.
    */
    void setPositionAngle(const int angle);
    ~ServoMotorImpl(void) { }

protected:
    #define MIN_ANGLE 0
    #define MAX_ANGLE 180
    #define DEF_ANGLE map(DEFAULT_PULSE_WIDTH, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH, MIN_ANGLE, MAX_ANGLE)

private:
    int angle;

};

#endif
