#ifndef __POTENTIOMETER__
#define __POTENTIOMETER__

#include "utils.h"

class Potentiometer {

public:
    Potentiometer(int pin);

    float getValue(void);

    virtual void sync(void);
    long getLastSyncTime(void);

protected:
    void updateSyncTime(long time);

private:
    long lastTimeSync;
    int pin;
    float value;

};

#endif
