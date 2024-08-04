#ifndef __ASYNC_FSM_EVENT_QUEUE__
#define __ASYNC_FSM_EVENT_QUEUE__

#include "utils.h"
#include "Event.h"
#include "MyQueue.h"

/**
 * Class representing an event queue.
 */
class EventQueue {

public:
    EventQueue(void);
    bool isEmpty(void);
    void enqueue(Event* ev);
    Event* dequeue(void);
    ~EventQueue(void);

private:
    MyQueue<Event *> *queue;

};

#endif
