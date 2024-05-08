#include "config.h"

#include "Led.h"
#include "SonarImpl.h"

Led ledGreen = Led(PIN_LED_GREEN);
Led ledRed = Led(PIN_LED_RED);
SonarImpl sonar = SonarImpl(PIN_SONAR_TRIG, PIN_SONAR_ECHO);
