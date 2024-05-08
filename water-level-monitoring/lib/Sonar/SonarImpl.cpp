#include "SonarImpl.h"

#define DEFAULT_TEMP 20 // ° C

/**
 * Retrieves speed of sound.
*/
static void _init_vs(float *vs, float *tempOld, float tempNew)
{
    *tempOld = tempNew;
    *vs = 331.45 + 0.62 * (*tempOld);
}

void SonarImpl::ConfigPins(const int trigPin, const int echoPin)
{
    this->trigPin = trigPin;
    this->echoPin = echoPin;
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

SonarImpl::SonarImpl(const int trigPin, const int echoPin)
{
    _init_vs(&vs, &(this->temperature), DEFAULT_TEMP);
    ConfigPins(trigPin, echoPin);
}

SonarImpl::SonarImpl(const int trigPin, const int echoPin, const float environmentTemperature)
{
    _init_vs(&vs, &temperature, environmentTemperature);
    ConfigPins(trigPin, echoPin);
}

float SonarImpl::getDistance(void)
{
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    /* Receiving the echo */
    float tUS = pulseIn(echoPin, HIGH);

    if (tUS <= 0) {
        return getErrorDistance();
    }
    return tUS * 0.017;
}
