#ifndef __TOGGLE_MODALITY_ASYNC_FSM_EVENT_SOURCE__
#define __TOGGLE_MODALITY_ASYNC_FSM_EVENT_SOURCE__

#include "Events/AsyncFSM.h"
#include "Button/ButtonImpl.h"

class ToggleModalityFSM : public AsyncFSM {

public:
    ToggleModalityFSM(Button *button, String *modality);
    void handleEvent(Event *ev);

private:
    Button* button;
    String *modality;

};

#endif