#ifndef __LOGGER__
#define __LOGGER__

#include "utils.h"

class Logger {

public:
    /**
     * Prints log prefix without newline.
    */
    void logstrt(void);
    /**
     * Prints debug prefix without newline.
    */
    void debugstrt(void);
    /**
     * Prints log message without prefix and newline.
    */
    void log(const String& msg);
    /**
     * Prints debug message without prefix and newline.
    */
    void debug(const String& msg);
    /**
     * Prints log newline.
    */
    void logln(void);
    /**
     * Prints debug newline.
    */
    void debugln(void);
    /**
     * Prints log message with format: prefix, message and newline.
    */
    void logln(const String& msg);
    /**
     * Prints debug message with format: prefix, message and newline.
    */
    void debugln(const String& msg);
    /**
     * Flushes text in the buffer.
    */
    void flush(void);

};

extern Logger MyLogger;

#endif
