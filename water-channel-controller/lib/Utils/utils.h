/**
 * General config file to define state of running code.
*/
#ifndef __UTILS__
#define __UTILS__

#include <Arduino.h>
#include <assert.h>

#define __DEBUG__

#define MIN_PERCENTAGE 0
#define MID_PERCENTAGE 50
#define MAX_PERCENTAGE 100

// #define TASK_BORN F("task born")
// #define TASK_INIT F("task init")
// #define TASK_DIE F("task die")
// #define TASK_STOP F("task stop")
// #define TASK_RESUME F("task resume")

#define PREFIX_LOG F("log> ")
#ifdef __DEBUG__
#define PREFIX_DEBUG F("debug> ")
#endif

#define XOR_SWAP(X, Y)  {\
                            (X) ^= (Y);\
                            (Y) ^= (X);\
                            (X) ^= (Y);\
                        }

#define TMP_SWAP(tmp, X, Y) {\
                                (tmp) = (X);\
                                (X) = (Y);\
                                (Y) = (tmp);\
                            }

#define ABS_DIFF(x, y) ((x) > (y) ? (x) - (y) : (y) - (x))

#define BAUD_RATE 9600

template<class T>
void swap(T &a, T &b) {
    T tmp = a;
    a = b;
    b = tmp;
}

void my_assert(unsigned char e);

#endif
