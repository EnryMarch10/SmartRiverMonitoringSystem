#include "Logger.h"
#include "MsgService.h"

Logger MyLogger;

void Logger::debugstrt(void) {
#ifdef __DEBUG__
    MyMsgService.sendMsg(PREFIX_DEBUG);
#endif
}

void Logger::logstrt(void) {
    MyMsgService.sendMsg(PREFIX_LOG);
}

void Logger::log(const String& msg) {
    MyMsgService.sendMsg(msg);
}

void Logger::logln(const String& msg) {
    MyMsgService.sendMsgLine(String(PREFIX_LOG) + msg);
}

void Logger::logln(void) {
    MyMsgService.sendMsgLine();
}

void Logger::debug(const String& msg) {
#ifdef __DEBUG__
    MyMsgService.sendMsg(msg);
#endif
}

void Logger::debugln(const String& msg) {
#ifdef __DEBUG__
    MyMsgService.sendMsgLine(String(PREFIX_DEBUG) + msg);
#endif
}

void Logger::debugln(void) {
#ifdef __DEBUG__
    MyMsgService.sendMsgLine();
#endif
}

void Logger::flush(void) {
    MyMsgService.flush();
}
