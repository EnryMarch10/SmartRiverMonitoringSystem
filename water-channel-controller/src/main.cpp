#include "config.h"

#include "Button/ButtonImpl.h"
#include "Lcd/LcdI2C.h"
#include "Potentiometer/Potentiometer.h"
#include "ServoMotor/Valve.h"
#include "Events/AsyncFSM.h"
#include "Serial/MsgService.h"
#include <Regexp.h>
#include <errno.h>

extern ButtonImpl button;
extern LcdI2C lcd;
extern Potentiometer potentiometer;
extern Valve valve;

extern int valvePercentage;
extern String remoteModality;
extern String modality;

// TODO:
// Right now there is no scheduler and everything is done inside the loop

class MyAsyncFSM : public AsyncFSM {

public:
    MyAsyncFSM(Button* button) {
        this->button = button;
        button->registerObserver(this);
    }

    void handleEvent(Event* ev) {
        if (ev->getType() == BUTTON_PRESSED_EVENT) {
            if (modality == MANUAL) {
                modality = AUTOMATIC;
            } else { // if (modality == AUTOMATIC)
                modality = MANUAL;
            }
        }
    }

private:
    Button* button;

};

MyAsyncFSM *myAsyncFSM;

const char pattern[] = "^(%S+)%s(.*)%s(%S+)$";

String lastModality = "";
int lastPosition = -1;

void setup() {
    init_config();
    myAsyncFSM = new MyAsyncFSM(&button);
}

void loop() {
    myAsyncFSM->checkEvents();
    if (MyMsgService.isMsgAvailable()) {
        Msg* msg = MyMsgService.receiveMsg();
        String content = msg->getContent();
        MatchState ms;
        char input[content.length() + 1];
        content.toCharArray(input, sizeof(input));
        ms.Target(input);
        if (ms.Match(pattern) == REGEXP_MATCHED) {
            if (ms.level == 3) {
                char MID[ms.capture[0].len + 1];
                ms.GetCapture(MID, 0);
                char command[ms.capture[1].len + 1];
                ms.GetCapture(command, 1);
                char value[ms.capture[2].len + 1];
                ms.GetCapture(value, 2);
                if (String(command) == F("set mode")) {
                    remoteModality = String(value);
                } else if (String(command) == F("set valve percentage")) {
                    errno = 0;
                    const int newPercentage = atoi(value);
                    if (errno == 0) {
                        if (newPercentage < MIN_PERCENTAGE || newPercentage > MAX_PERCENTAGE) {
                            MyConsole.logln(String(MID) + F(" ERROR invalid percentage value"));
                        } else {
                            valvePercentage = newPercentage;
                            MyConsole.debugln(String(MID) + F(" OK new valve level set to ") + valvePercentage + F(" %"));
                        }
                    } else {
                        MyConsole.logln(String(MID) + F(" ERROR invalid percentage format (not a number)"));
                    }
                } else {
                    MyConsole.logln(String(MID) + F(" ERROR invalid command"));
                }
            } else {
                MyConsole.logln(F("ERROR invalid message (correct format 'MID command value')"));
            }
        } else {
            MyConsole.logln(F("ERROR regex unmatched"));
        }
        delete msg;
    }

    if (modality == MANUAL) {
        valvePercentage = potentiometer.getValue();
        // MyConsole.logln(String(F("Potentiometer percentage set to ")) + valvePercentage);
    }

    valve.setPositionPercentage(valvePercentage);
    // TODO: this would block the loop, this behavior is reached even without this code
    // const unsigned long start = millis();
    // while(valve.readPositionPercentage() != valvePercentage) {
    //     const unsigned long stop = millis();
    //     if (stop - start > VALVE_STEP_TIMEOUT) {
    //         MyConsole.debugln(String(F("WARNING valve timeout occurred (")) + VALVE_STEP_TIMEOUT + F(" ms)"));
    //         break;
    //     }
    // }

    String nextModality;
    const int nextPosition = valve.readPositionPercentage();
    if (modality == MANUAL) {
        nextModality = MANUAL;
    } else { // if (modality == AUTOMATIC)
        nextModality = remoteModality;
    }

    static unsigned long lastMsgTime = 0;
    static const long unsigned period = 500;
    const unsigned long now = millis();
    if (now - lastMsgTime > period && (nextPosition != lastPosition || nextModality != lastModality)) {
        lastMsgTime = now;
        lastModality = nextModality;
        lastPosition = nextPosition;
        lcd.clear();
        lcd.write(nextModality + F(" - ") + nextPosition);
    }
}
    