#include "EventSource.h"
#include "InterruptDispatcher.h"

EventSource::EventSource(const int pin) {
    interruptDispatcher.bind(pin, this);
}

void EventSource::registerObserver(EventsObserver* observer) {
    this->observer = observer;
}

void EventSource::generateEvent(Event* ev) {
    if (observer != NULL) {
        observer->notifyEvent(ev);
    }
}
