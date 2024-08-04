#ifndef __ASYNC_FSM_EVENT__
#define __ASYNC_FSM_EVENT__

#include "utils.h"

/**
 * Class representing an event.
 */
class Event {

public:
    Event(int type);
    int getType(void);
    ~Event(void) { }

private:
    int type;

};

#endif
