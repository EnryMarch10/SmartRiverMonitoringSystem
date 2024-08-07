#include "config.h"

#include "Serial/MsgService.h"
#include "Button/ButtonImpl.h"
#include "Lcd/LcdI2C.h"
#include "Potentiometer/Potentiometer.h"
#include "ServoMotor/Valve.h"
#include <FSMs/ToggleModalityFSM.h>

ButtonImpl button = ButtonImpl(PIN_BUTTON);
LcdI2C lcd = LcdI2C(LCD_ADDRESS);
Potentiometer potentiometer = Potentiometer(PIN_POTENTIOMETER, MIN_PERCENTAGE, MAX_PERCENTAGE);
Valve valve = Valve(PIN_SERVO_MOTOR);

ToggleModalityFSM *toggleModalityFSM;

String remoteModalityOld;
String remoteModality;
String modality;
int valvePercentage;

void init_config(void)
{
    MyMsgService.init();
    lcd.init();
    lcd.on();
    valve.on();
    remoteModalityOld = "";
    remoteModality = AUTOMATIC;
    modality = AUTOMATIC;
    const unsigned long start = millis();
    while(valve.readPosition() != DEFAULT_PULSE_WIDTH) {
        const unsigned long stop = millis();
        if (stop - start > VALVE_INIT_TIMEOUT) {
                MyConsole.debugln(String(F("Valve timeout occurred in initialization (")) + VALVE_INIT_TIMEOUT + F(" ms)"));
            break;
        }
    }
    valvePercentage = valve.readPositionPercentage();
    toggleModalityFSM = new ToggleModalityFSM(&button, &modality);
}
