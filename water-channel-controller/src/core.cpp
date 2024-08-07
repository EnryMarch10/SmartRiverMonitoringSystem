#include <Serial/MsgService.h>
#include <FSMs/ToggleModalityFSM.h>
#include <Regexp.h>
#include <errno.h>

#include "config.h"
#include "Lcd/LcdI2C.h"
#include "Potentiometer/Potentiometer.h"
#include "ServoMotor/Valve.h"

#define LCD_MAX_REFRESH_RATE 500 // ms

extern ToggleModalityFSM *toggleModalityFSM;

extern LcdI2C lcd;
extern Potentiometer potentiometer;
extern Valve valve;

extern int valvePercentage;
extern String remoteModality;
extern String modality;

String lastModality = "";
int lastPosition = -1;

static const char *pattern = "^(%S+)%s(.*)%s(%S+)$";

static void _check_message(void) {
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
                    if (errno == 0 && newPercentage >= MIN_PERCENTAGE && newPercentage <= MAX_PERCENTAGE) {
                        valvePercentage = newPercentage;
                        MyConsole.debugln(String(MID) + F(" OK new valve level set to ") + valvePercentage + F(" %"));
                    }
                }
            }
        }
        delete msg;
    }
}

static void _set_valve_level(void) {
    if (modality == MANUAL) {
        valvePercentage = potentiometer.getValue();
    }
    valve.setPositionPercentage(valvePercentage);
}

static void _update_display(void) {
    static unsigned long lastMsgTime = 0;

    const int nextPosition = valve.readPositionPercentage();
    const String nextModality = modality == MANUAL ? MANUAL : remoteModality;
    const unsigned long now = millis();
    if (now - lastMsgTime > LCD_MAX_REFRESH_RATE && (nextPosition != lastPosition || nextModality != lastModality)) {
        lastMsgTime = now;
        lastModality = nextModality;
        lastPosition = nextPosition;
        lcd.clear();
        lcd.write(nextModality + F(" - ") + nextPosition);
    }
}

void iterate() {
    toggleModalityFSM->checkEvents();
    _check_message();
    _set_valve_level();
    _update_display();
}
