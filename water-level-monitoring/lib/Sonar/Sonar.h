#ifndef __SONAR__
#define __SONAR__

#include "utils.h"

class Sonar {

public:
    /**
     * Value returned when the distance is too big to be detected from the Sonar.
    */
    static float  getErrorDistance(void)
    {
        return -1.0;
    }
    /**
     * Retrieves distance in meters or getErrorIndex() if something has gone wrong.
    */
    virtual float getDistance(void) = 0;
    virtual ~Sonar(void) { }

};

#endif
