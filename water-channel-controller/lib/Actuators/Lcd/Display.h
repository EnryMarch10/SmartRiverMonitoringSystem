#ifndef __DISPLAY__
#define __DISPLAY__

#include "utils.h"

class Display {

public:
    virtual void init(void) = 0;
    virtual char getRows(void) = 0;
    virtual char getColumns(void) = 0;
    virtual void on(void) = 0;
    virtual void off(void) = 0;
    virtual void clear(void) = 0;
    virtual void write(const String &string) = 0;
    virtual ~Display(void) { }

};

#endif
