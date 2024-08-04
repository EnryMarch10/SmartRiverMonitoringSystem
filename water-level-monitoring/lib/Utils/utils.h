/**
 * General config file to define state of running code.
*/
#ifndef __UTILS__
#define __UTILS__

#include <Arduino.h>

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

template<class T>
void swap(T &a, T &b)
{
    T tmp = a;
    a = b;
    b = tmp;
}

#define BAUD_RATE 9600

#endif
