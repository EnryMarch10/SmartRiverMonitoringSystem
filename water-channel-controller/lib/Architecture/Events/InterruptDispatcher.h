#ifndef __ASYNC_FSM_INTERRUPT_DISPATCHER__
#define __ASYNC_FSM_INTERRUPT_DISPATCHER__

#include "utils.h"
#include "EventSource.h"

#define NUM_PINS 13

/**
 * Class binding Interrupts to Event Sources.
 */
class InterruptDispatcher {

public:
    InterruptDispatcher(void);
    /**
     * Binds an interrupt to an event source.
     */
    void bind(const int pin, EventSource* src);
    /**
     * Notifies that an interrupt as occurred at the specified pin.
     */
    void notifyInterrupt(const int pin);
    ~InterruptDispatcher(void) { }

private:
    EventSource* sourceRegisteredOnPin[NUM_PINS];
    void (*notifyFunctions[NUM_PINS])(void) = { };

    static void notifyInterrupt_0(void);
    static void notifyInterrupt_1(void);
    static void notifyInterrupt_2(void);
    static void notifyInterrupt_3(void);
    static void notifyInterrupt_4(void);
    static void notifyInterrupt_5(void);
    static void notifyInterrupt_6(void);
    static void notifyInterrupt_7(void);
    static void notifyInterrupt_8(void);
    static void notifyInterrupt_9(void);
    static void notifyInterrupt_10(void);
    static void notifyInterrupt_11(void);
    static void notifyInterrupt_12(void);
    static void notifyInterrupt_13(void);

};

extern InterruptDispatcher interruptDispatcher;

#endif
