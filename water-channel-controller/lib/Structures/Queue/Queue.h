#ifndef __QUEUE__H
#define __QUEUE__H

#include "utils.h"

template<typename T>
class Queue {

public:
    Queue(void);
    bool isEmpty(void);
    bool containsSomething(void);
    void enqueue(const T& obj);
    T dequeue(void);
    ~Queue(void);

private:
    typedef struct Node {
        T item;
        struct Node* next;
        struct Node* prev;
    }
    Node;
    unsigned n;
    Node* first;
    Node* last;

};

#include "Queue.cpp"

#endif // __QUEUE__H
