#ifndef __ASYNC_FSM_EVENT_SOURCE__
#define __ASYNC_FSM_EVENT_SOURCE__

#include "utils.h"
#include "EventsObserver.h"

/**
 * Abstract class representing an event source, generating Events (Interrupts) observed by an EventsObserver.
 * Manages the Interrupts -> Events (I/O) conversion, mapping Interrupts as Events.
 */
class EventSource {

public:
    /**
     * Constructor that binds this class to be notified when an Interrupt occurs in the specified pin.
     */
    EventSource(const int pin);
    /**
     * Register an Observer of Events to be notified by this class when an Event occurs.
     */
    void registerObserver(EventsObserver *observer);
    /**
     * Notifies that an Interrupt has occurred on the specified pin.
     * Inside you should notify the Observer of Events with the generation of a new Event.
     */
    virtual void notifyInterrupt(const int pin) = 0;
    ~EventSource(void) { }

protected:
    /**
     * Called to generate an event to be observed by the Observer of Events.
     */
    void generateEvent(Event* ev);

private:
    EventsObserver* observer;

};

#endif
