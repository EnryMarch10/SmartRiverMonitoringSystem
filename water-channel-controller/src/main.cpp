#include "config.h"

extern void iterate();

void setup() {
    init_config();
}

void loop() {
    iterate();
}
