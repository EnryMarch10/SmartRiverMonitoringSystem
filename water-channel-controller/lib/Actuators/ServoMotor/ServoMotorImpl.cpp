#include "ServoMotorImpl.h"

#define TOLERANCE 5 // degrees

void ServoMotorImpl::init(void) {
    angle = DEF_ANGLE;
}

int ServoMotorImpl::readPositionAngle(void) {
    const int value = map(readPosition(), MIN_PULSE_WIDTH, MAX_PULSE_WIDTH, MIN_ANGLE, MAX_ANGLE);
    if (ABS_DIFF(angle, value) > TOLERANCE) {
        return value;
    }
    return angle;
}

void ServoMotorImpl::setPositionAngle(const int angle) {
#ifdef __DEBUG__
    assert(angle >= MIN_ANGLE && angle <= MAX_ANGLE);
#endif
    pMotor->write(map(angle, MIN_ANGLE, MAX_ANGLE, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH));
    this->angle = angle;
}
