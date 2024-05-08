#ifndef __GATE__
#define __GATE__

class Gate {

public:
    /**
     * Opens the gate in atomic way.
     * Returns if the gate is fully open or not.
    */
    virtual bool open(void) = 0;
    /**
     * Closes the gate in atomic way.
     * Returns if the gate is fully close or not.
    */
    virtual bool close(void) = 0;
    virtual void on(void) = 0;
    virtual void off(void) = 0;
    virtual ~Gate(void) { }

};

#endif
