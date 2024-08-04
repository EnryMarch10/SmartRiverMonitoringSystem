#ifndef __LCD__
#define __LCD__

#include <LiquidCrystal_I2C.h>
#include "Display.h"

class LcdI2C: public Display {

public:
    LcdI2C(const int address);
    LcdI2C(const int address, const int rows, const int columns);
    void init(void);
    char getRows(void);
    char getColumns(void);
    void on(void);
    void off(void);
    void clear(void);
    void write(const String &string);
    ~LcdI2C(void);

private:
    enum {ON, OFF} state;
    char rows;
    char columns;
    LiquidCrystal_I2C *pLcd;

};

#endif
