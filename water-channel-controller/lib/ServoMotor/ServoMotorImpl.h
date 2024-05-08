#ifndef __SERVO_MOTOR_IMPL__
#define __SERVO_MOTOR_IMPL__

#include "ServoMotor.h"
#include <ServoTimer2.h>

class ServoMotorImpl: public ServoMotor {

public:
    ServoMotorImpl(const int pin);
    // SERVO MOTOR
    void on(void);
    int readPosition(void);
    void setPosition(const int angle);
    void off(void);
    // GATE
    bool open(void);
    bool close(void);
    ~ServoMotorImpl(void);

private:
    bool isFullyOpen(void);
    bool isFullyClose(void);
    int pin;
    int angle;
    ServoTimer2 *pMotor;

};

#endif
