#include "utils.h"

void my_assert(unsigned char e) {
#ifdef __DEBUG__
    assert(e);
#endif
}
