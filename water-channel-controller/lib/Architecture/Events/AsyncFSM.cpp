#include "AsyncFSM.h"

AsyncFSM::AsyncFSM(void) { }

void AsyncFSM::notifyEvent(Event* ev) {
    eventQueue.enqueue(ev);
}

void AsyncFSM::checkEvents(void) {
    noInterrupts();
    bool isEmpty = eventQueue.isEmpty();
    interrupts();

    if (!isEmpty) {
        noInterrupts();
        Event* ev = eventQueue.dequeue();
        interrupts();

        my_assert(ev != NULL);
        handleEvent(ev);
        delete ev;
    }
}
