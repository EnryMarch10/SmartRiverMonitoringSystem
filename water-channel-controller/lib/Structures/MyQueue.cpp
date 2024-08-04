#ifndef __QUEUE__CPP
#define __QUEUE__CPP

#include "MyQueue.h"

template <typename T>
MyQueue<T>::MyQueue(void) {
    n = 0;
    first = last = NULL;
}

template <typename T>
bool MyQueue<T>::isEmpty(void) {
    if (first != NULL) {
        my_assert(n != 0);
        return false;
    }
    return true;
}

template <typename T>
bool MyQueue<T>::containsSomething(void) {
    return !isEmpty();
}

template <typename T>
void MyQueue<T>::enqueue(const T& obj) {
    Node* tmp = NULL;
    tmp = (Node *) malloc(sizeof(*tmp));
    my_assert(tmp != NULL);
    tmp->item = obj;

    if ((first == NULL) && (last == NULL)) {
        tmp->next = tmp->prev = tmp;
        first = tmp;
    } else if (last == NULL) {
        tmp->next = tmp->prev = first;
        first->prev = first->next = tmp;
        last = tmp;
    } else {
        my_assert(first != NULL);
        tmp->next = last;
        tmp->prev = first;
        last->prev = first->next = tmp;
        last = tmp;
    }
    n++;
}

template <typename T>
T MyQueue<T>::dequeue(void) {
    T result;
    Node* tmp;
    my_assert(first != NULL);
    result = first->item;

    if ((first != NULL) && (last != NULL)) {
        last->prev = first->prev;
        first->prev->next = last;
        tmp = first;
        if (first->prev == last) {
            first = last;
            last = NULL;
        } else {
            first = first->prev;
        }
        free(tmp);
        n--;
    } else if (first != NULL) {
        free(first);
        first = NULL;
        n--;
    }
    return result;
}

template <typename T>
MyQueue<T>::~MyQueue(void) {
    while (!isEmpty()) {
        dequeue();
    }
    my_assert((first == NULL) && (last == NULL));
}

#endif // __QUEUE__CPP
