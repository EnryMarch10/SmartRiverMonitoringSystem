#ifndef __BUTTON__
#define __BUTTON__

#include "utils.h"
#include "Events/Event.h"
#include "Events/EventSource.h"

#define BUTTON_PRESSED_EVENT 1
#define BUTTON_RELEASED_EVENT 2

class Button : public EventSource {

public:
    Button(const int pin) : EventSource(pin) { }
    virtual bool isPressed(void) = 0;
    virtual ~Button(void) { }

};

class ButtonPressed: public Event {

public:
    ButtonPressed(Button *source) : Event(BUTTON_PRESSED_EVENT) {
        this->source = source;
    }
    Button *getSource(void) {
        return source;
    }

private:
    Button *source;

};

class ButtonReleased: public Event {

public:
    ButtonReleased(Button *source) : Event(BUTTON_RELEASED_EVENT) {
        this->source = source;
    }
    Button *getSource(void) {
        return source;
    }

private:
    Button *source;

};

#endif
