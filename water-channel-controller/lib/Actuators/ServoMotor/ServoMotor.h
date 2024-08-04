#ifndef __SERVO_MOTOR__
#define __SERVO_MOTOR__

#include "utils.h"
#include <ServoTimer2.h>

class ServoMotor {

public:
    /**
     * Constructor.
     */
    ServoMotor(const int pin) {
        this->pin = pin;
        pMotor = new ServoTimer2();
    }
    /**
     * Turns on the motor.
    */
    void on(void) {
        pMotor->attach(pin);
        // TODO: controlla se superfluo
        pMotor->write(DEFAULT_PULSE_WIDTH);
        init();
    }
    virtual void init(void) = 0;
    int readPosition(void) {
        return pMotor->read();
    }
    void setPosition(const int position) {
        pMotor->write(position);
    }
    /**
     * Turns off the motor.
     */
    void off(void) {
        pMotor->detach();
    }
    virtual ~ServoMotor(void) {
        delete pMotor;
    }

protected:
    ServoTimer2 *pMotor;

private:
    int pin;

};

#endif
