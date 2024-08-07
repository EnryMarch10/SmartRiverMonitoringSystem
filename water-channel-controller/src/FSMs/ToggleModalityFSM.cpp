#include "FSMs/ToggleModalityFSM.h"
#include "config.h"

ToggleModalityFSM::ToggleModalityFSM(Button* button, String *modality) {
    this->button = button;
    this->modality = modality;
    button->registerObserver(this);
}

void ToggleModalityFSM::handleEvent(Event* ev) {
    if (ev->getType() == BUTTON_PRESSED_EVENT) {
        if (*modality == MANUAL) {
            *modality = AUTOMATIC;
        } else { // if (modality == AUTOMATIC)
            *modality = MANUAL;
        }
    }
}
