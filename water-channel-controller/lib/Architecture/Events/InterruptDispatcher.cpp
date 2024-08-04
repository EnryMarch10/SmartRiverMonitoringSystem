#include "InterruptDispatcher.h"
#include <EnableInterrupt.h>

/* The singleton interrupt dispatcher, binding interrupts to event sources */
InterruptDispatcher interruptDispatcher;

/*
 * Functions called by the interrupt handlers, used to notify interrupts to
 * to the interrupt dispatcher
 */

void InterruptDispatcher::notifyInterrupt_0(void) { interruptDispatcher.notifyInterrupt(0); }
void InterruptDispatcher::notifyInterrupt_1(void) { interruptDispatcher.notifyInterrupt(1); }
void InterruptDispatcher::notifyInterrupt_2(void) { interruptDispatcher.notifyInterrupt(2); }
void InterruptDispatcher::notifyInterrupt_3(void) { interruptDispatcher.notifyInterrupt(3); }
void InterruptDispatcher::notifyInterrupt_4(void) { interruptDispatcher.notifyInterrupt(4); }
void InterruptDispatcher::notifyInterrupt_5(void) { interruptDispatcher.notifyInterrupt(5); }
void InterruptDispatcher::notifyInterrupt_6(void) { interruptDispatcher.notifyInterrupt(6); }
void InterruptDispatcher::notifyInterrupt_7(void) { interruptDispatcher.notifyInterrupt(7); }
void InterruptDispatcher::notifyInterrupt_8(void) { interruptDispatcher.notifyInterrupt(8); }
void InterruptDispatcher::notifyInterrupt_9(void) { interruptDispatcher.notifyInterrupt(9); }
void InterruptDispatcher::notifyInterrupt_10(void) { interruptDispatcher.notifyInterrupt(10); }
void InterruptDispatcher::notifyInterrupt_11(void) { interruptDispatcher.notifyInterrupt(11); }
void InterruptDispatcher::notifyInterrupt_12(void) { interruptDispatcher.notifyInterrupt(12); }
void InterruptDispatcher::notifyInterrupt_13(void) { interruptDispatcher.notifyInterrupt(13); }

InterruptDispatcher::InterruptDispatcher(void) {
    notifyFunctions[0] = notifyInterrupt_0;
    notifyFunctions[1] = notifyInterrupt_1;
    notifyFunctions[2] = notifyInterrupt_2;
    notifyFunctions[3] = notifyInterrupt_3;
    notifyFunctions[4] = notifyInterrupt_4;
    notifyFunctions[5] = notifyInterrupt_5;
    notifyFunctions[6] = notifyInterrupt_6;
    notifyFunctions[7] = notifyInterrupt_7;
    notifyFunctions[8] = notifyInterrupt_8;
    notifyFunctions[9] = notifyInterrupt_9;
    notifyFunctions[10] = notifyInterrupt_10;
    notifyFunctions[11] = notifyInterrupt_11;
    notifyFunctions[12] = notifyInterrupt_12;
    notifyFunctions[13] = notifyInterrupt_13;
}

void InterruptDispatcher::bind(const int pin, EventSource* src) {
    sourceRegisteredOnPin[pin] = src;
    enableInterrupt(pin, notifyFunctions[pin], CHANGE);
}

void InterruptDispatcher::notifyInterrupt(const int pin) {
    sourceRegisteredOnPin[pin]->notifyInterrupt(pin);
}
