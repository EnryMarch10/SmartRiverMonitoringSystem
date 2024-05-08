#include "ServoMotorImpl.h"

#define MIN_ANGLE 0
#define DEF_ANGLE map(DEFAULT_PULSE_WIDTH, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH, MIN_ANGLE, MAX_ANGLE)
#define MAX_ANGLE 180

ServoMotorImpl::ServoMotorImpl(const int pin)
{
    this->pin = pin;
    pMotor = new ServoTimer2();
    angle = DEF_ANGLE;
} 

// SERVO

void ServoMotorImpl::on(void)
{
    pMotor->attach(pin);    
}

int ServoMotorImpl::readPosition(void)
{
    return angle;              
}

void ServoMotorImpl::setPosition(const int angle)
{
#ifdef __DEBUG__
    assert(angle >= MIN_ANGLE && angle <= MAX_ANGLE);
#endif
    pMotor->write(map(angle, MIN_ANGLE, MAX_ANGLE, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH));
    this->angle = angle;
}

void ServoMotorImpl::off(void)
{
    pMotor->detach();    
}

ServoMotorImpl::~ServoMotorImpl(void)
{
    delete pMotor;
}

// GATE

bool ServoMotorImpl::open(void)
{
    if (!isFullyOpen()) {
        setPosition(min(readPosition() + 5, MAX_ANGLE));
    }
    return isFullyOpen();
}

bool ServoMotorImpl::isFullyOpen(void)
{
    return readPosition() == MAX_ANGLE;
}

bool ServoMotorImpl::close(void)
{
    if (!isFullyClose()) {
        setPosition(max(readPosition() - 5, MIN_ANGLE));
    }
    return isFullyClose();
}

bool ServoMotorImpl::isFullyClose(void)
{
    return readPosition() == MIN_ANGLE;
}
