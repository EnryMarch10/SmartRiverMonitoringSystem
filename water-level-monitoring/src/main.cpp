#include "config.h"
#include "Led.h"
#include "SonarImpl.h"

#define MSG_BUFFER_SIZE 50

extern SonarImpl sonar;

extern PubSubClient mqtt_client;

extern const char *mqtt_topic_period;
extern const char *mqtt_topic_water_level;

extern long unsigned period;

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
    errno = 0;
    char *end;
    char *message = (char *) payload;
    const unsigned long newPeriod = strtoul(message, &end, 10);
    if (message != end && errno != ERANGE) {
        period = newPeriod;
#ifdef __DEBUG__
        Serial.println(String("[MQTT_CALLBACK] New period ok: ") + period);
#endif
    } else {
        Serial.println("[MQTT_CALLBACK] Message period format error");
    }
}

void setup() {
    // TODO: Replace first 2 parameters with your WiFi name and password
    init_config("WIFI-ssid", "WIFI-password", mqtt_callback);
    mqtt_connect();
}

void loop() {
    static char msg[MSG_BUFFER_SIZE];
    static unsigned long lastMsgTime = 0;

    if (!mqtt_client.connected()) {
        mqtt_connect();
    }
    mqtt_client.loop();

    const unsigned long now = millis();
    if (now - lastMsgTime > period) {
        lastMsgTime = now;

        const float water_level = sonar.getDistance();
        if (water_level != sonar.getErrorDistance()) {
            /* creating a msg in the buffer */
            snprintf(msg, MSG_BUFFER_SIZE, "%f", water_level);
#ifdef __DEBUG__
            Serial.println(String("[APP] Publishing message on topic `") + mqtt_topic_water_level + "`: " + msg + " at " + now / 1000.0 + " s");
#endif
            mqtt_client.publish(mqtt_topic_water_level, msg);
        } else {
            Serial.println("[APP] Sonar unable to detect correct water level");
        }
    }
}
