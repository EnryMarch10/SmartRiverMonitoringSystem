#include "LcdI2C.h"

#define DEFAULT_ROWS 2
#define DEFAULT_COLUMNS 16

LcdI2C::LcdI2C(const int address) {
    rows = DEFAULT_ROWS;
    columns = DEFAULT_COLUMNS;
    pLcd = new LiquidCrystal_I2C(address, columns, rows);
}

LcdI2C::LcdI2C(const int address, const int rows, const int columns) {
    this->rows = rows;
    this->columns = columns;
    pLcd = new LiquidCrystal_I2C(address, this->columns, this->rows);
}

void LcdI2C::init(void) {
    pLcd->init();
    off();
    state = OFF;
}

char LcdI2C::getRows(void) {
    return rows;
}

char LcdI2C::getColumns(void) {
    return columns;
}

void LcdI2C::on(void) {
    if (state == OFF) {
        pLcd->backlight();
        pLcd->display();
        state = ON;
    } else {
        pLcd->clear();
    }
}

void LcdI2C::off(void) { 
    if (state == ON) {
        pLcd->clear();
        pLcd->noDisplay();
        pLcd->noBacklight();
        state = OFF;
    }
}

void LcdI2C::clear(void) {
    pLcd->clear();
}

void LcdI2C::write(const String &string) {
    pLcd->setCursor(0, 0);
    if (string.length() > (unsigned) rows) {
        pLcd->print(string.substring(0, columns));
        pLcd->setCursor(0, 1);
        pLcd->print(string.substring(columns, string.length()));
    } else {
        pLcd->print(string);
    }
}

LcdI2C::~LcdI2C(void) {
    delete pLcd;
}
