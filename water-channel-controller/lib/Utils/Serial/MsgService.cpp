#include "MsgService.h"

#define BUFFER_SIZE 256

static String content;

MsgServiceClass MyMsgService;

bool MsgServiceClass::isMsgAvailable(void) {
    return msgAvailable;
}

Msg* MsgServiceClass::receiveMsg(void) {
    if (msgAvailable) {
        Msg* msg = currentMsg;
        msgAvailable = false;
        currentMsg = NULL;
        content = "";
        return msg;
    } else {
        return NULL;
    }
}

void MsgServiceClass::init(void) {
    Serial.begin(BAUD_RATE);
    content.reserve(BUFFER_SIZE);
    content = "";
    currentMsg = NULL;
    msgAvailable = false;  
}

void MsgServiceClass::sendMsg(const String& msg) { 
    Serial.print(msg);
}

void MsgServiceClass::sendMsgLine(const String& msg) { 
    Serial.println(msg);
}

void MsgServiceClass::sendMsgLine(void) { 
    Serial.println();
}

void MsgServiceClass::flush(void) { 
    Serial.flush();
}

void serialEvent(void) {
    while (Serial.available()) {
        char c = (char) Serial.read();
        if (c == '\n') {
            MyMsgService.currentMsg = new Msg(content);
            MyMsgService.msgAvailable = true;     
        } else {
            content += c; 
        }
    }
}

bool MsgServiceClass::isMsgAvailable(Pattern& pattern) {
    return (msgAvailable && pattern.match(*currentMsg));
}

Msg *MsgServiceClass::receiveMsg(Pattern& pattern) {
    if (msgAvailable && pattern.match(*currentMsg)) {
        Msg *msg = currentMsg;
        msgAvailable = false;
        currentMsg = NULL;
        content = "";
        return msg;
    } else {
        return NULL;
    }
}
