#ifndef __MSG_SERVICE__
#define __MSG_SERVICE__

#include "utils.h"

class Msg {
    String content;

public:
    Msg(const String content) {
        this->content = content;
    }
    
    String getContent(void) {
        return content;
    }

};

class Pattern {

public:
    virtual boolean match(const Msg &m) = 0;

};

class MsgServiceClass {

public:
    Msg* currentMsg;
    bool msgAvailable;

    void init(void);
    bool isMsgAvailable(void);
    bool isMsgAvailable(Pattern& pattern);
    Msg *receiveMsg(void);
    Msg *receiveMsg(Pattern& pattern);
    void sendMsg(const String& msg);
    void sendMsgLine(const String& msg);
    void sendMsgLine(void);
    void flush(void);

};

extern MsgServiceClass MyMsgService;

#endif
