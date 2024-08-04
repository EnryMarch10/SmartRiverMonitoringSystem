#ifndef __ASYNC_FSM_OBSERVER__
#define __ASYNC_FSM_OBSERVER__

#include "utils.h"
#include "Event.h"

/**
 * Class representing event observers, observing Event.
 */
class EventsObserver {

public:
    /**
     * Notifies that an event has occurred.
     */
    virtual void notifyEvent(Event* ev) = 0;

};

#endif
