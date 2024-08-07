#include "Console.h"
#include "MsgService.h"

Console MyConsole;

#define PREFIX_INFO F("INFO: ")
#define PREFIX_WARNING F("WARNING: ")
#define PREFIX_ERROR F("ERROR: ")

#define PREFIX_LOG F("log> ")
#ifdef __DEBUG__
#define PREFIX_DEBUG F("debug> ")
#endif

void Console::prefixInfo(void) {
    MyMsgService.sendMsg(PREFIX_INFO);
}

void Console::prefixWarning(void) {
    MyMsgService.sendMsg(PREFIX_WARNING);
}

void Console::prefixError(void) {
    MyMsgService.sendMsg(PREFIX_ERROR);
}

void Console::prefixLog(void) {
    MyMsgService.sendMsg(PREFIX_LOG);
}

void Console::prefixDebug(void) {
#ifdef __DEBUG__
    MyMsgService.sendMsg(PREFIX_DEBUG);
#endif
}

void Console::printInfo(const String& msg) {
    MyMsgService.sendMsg(msg);
}

void Console::printlnInfo(const String& msg) {
    MyMsgService.sendMsgLine(String(PREFIX_INFO) + msg);
}

void Console::printWarning(const String& msg) {
    MyMsgService.sendMsg(msg);
}

void Console::printlnWarning(const String& msg) {
    MyMsgService.sendMsgLine(String(PREFIX_WARNING) + msg);
}

void Console::printErr(const String& msg) {
    MyMsgService.sendMsg(msg);
}

void Console::printlnErr(const String& msg) {
    MyMsgService.sendMsgLine(String(PREFIX_ERROR) + msg);
}

void Console::print(const String& msg) {
    MyMsgService.sendMsg(msg);
}

void Console::println(void) {
    MyMsgService.sendMsgLine();
}

void Console::println(const String& msg) {
    MyMsgService.sendMsgLine(msg);
}

void Console::log(const String& msg) {
    MyMsgService.sendMsg(msg);
}

void Console::logln(void) {
    MyMsgService.sendMsgLine();
}

void Console::logln(const String& msg) {
    MyMsgService.sendMsgLine(String(PREFIX_LOG) + msg);
}

void Console::debug(const String& msg) {
#ifdef __DEBUG__
    MyMsgService.sendMsg(msg);
#endif
}

void Console::debugln(void) {
#ifdef __DEBUG__
    MyMsgService.sendMsgLine();
#endif
}

void Console::debugln(const String& msg) {
#ifdef __DEBUG__
    MyMsgService.sendMsgLine(String(PREFIX_DEBUG) + msg);
#endif
}

void Console::flush(void) {
    MyMsgService.flush();
}
