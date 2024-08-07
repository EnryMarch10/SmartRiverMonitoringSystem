#include "EventQueue.h"

EventQueue::EventQueue(void) {
    queue = new Queue<Event *>();
}

bool EventQueue::isEmpty(void) {
    return queue->isEmpty();
}

void EventQueue::enqueue(Event* ev) {
    queue->enqueue(ev);
}

Event* EventQueue::dequeue(void) {
    return queue->dequeue();
}

EventQueue::~EventQueue(void)
{
    delete queue;
}
