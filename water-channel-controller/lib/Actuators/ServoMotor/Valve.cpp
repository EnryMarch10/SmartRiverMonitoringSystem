#include "Valve.h"

#define DEF_PERCENTAGE MID_PERCENTAGE
#define TOLERANCE 4 // percent
#define STEP_SIZE 1 // percent

void Valve::init(void) {
    percentage = DEF_PERCENTAGE;
}

int Valve::readPositionPercentage(void) {
    const int value = map(readPosition(), MIN_PULSE_WIDTH, MAX_PULSE_WIDTH, MIN_PERCENTAGE, MAX_PERCENTAGE);
    if (ABS_DIFF(percentage, value) > TOLERANCE) {
        return value;
    }
    return percentage;
}

void Valve::setPositionPercentage(const int percentage) {
#ifdef __DEBUG__
    assert(percentage >= MIN_PERCENTAGE && percentage <= MAX_PERCENTAGE);
#endif
    const int position = readPositionPercentage();
    if (ABS_DIFF(percentage, position) > TOLERANCE) { // Compares the actual position to the specified percentage using a tolerance
        if (percentage > position) {
            this->percentage = min(position + STEP_SIZE, MAX_PERCENTAGE);
        } else { // if (percentage < position)
            this->percentage = max(position - STEP_SIZE, MIN_PERCENTAGE);
        }
        setPosition(map(this->percentage, MIN_PERCENTAGE, MAX_PERCENTAGE, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH));
    }
}
