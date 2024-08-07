#ifndef __CONSOLE__
#define __CONSOLE__

#include "utils.h"

class Console {

public:
    /**
     * Prints LOG prefix.
    */
    void prefixInfo(void);
    /**
     * Prints WARNING prefix.
    */
    void prefixWarning(void);
    /**
     * Prints ERROR prefix.
    */
    void prefixError(void);
    /**
     * Prints log prefix.
    */
    void prefixLog(void);
    /**
     * Prints debug prefix.
    */
    void prefixDebug(void);
    /**
     * Prints info message without newline.
     */
    void printInfo(const String &msg);
    /**
     * Prints info message with newline.
    */
    void printlnInfo(const String& msg);
    /**
     * Prints warning message without newline.
     */
    void printWarning(const String &msg);
    /**
     * Prints warning message with newline.
    */
    void printlnWarning(const String& msg);
    /**
     * Prints error message without newline.
     */
    void printErr(const String &msg);
    /**
     * Prints error message with newline.
    */
    void printlnErr(const String& msg);
    /**
     * Prints message without newline.
     */
    void print(const String &msg);
    /**
     * Prints newline.
    */
    void println(void);
    /**
     * Prints message with newline.
    */
    void println(const String& msg);
    /**
     * Prints log message without prefix and newline.
     */
    void log(const String& msg);
    /**
     * Prints log newline.
    */
    void logln(void);
    /**
     * Prints log message with format: prefix, message and newline.
    */
    void logln(const String& msg);
    /**
     * Prints debug message without prefix and newline.
    */
    void debug(const String& msg);
    /**
     * Prints debug newline.
    */
    void debugln(void);
    /**
     * Prints debug message with format: prefix, message and newline.
    */
    void debugln(const String& msg);
    /**
     * Flushes text in the buffer.
    */
    void flush(void);

};

extern Console MyConsole;

#endif
