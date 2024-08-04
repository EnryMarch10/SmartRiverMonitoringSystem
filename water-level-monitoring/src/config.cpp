#include "config.h"

#include "Led.h"
#include "SonarImpl.h"

#include <WiFi.h>
#include <WiFiClientSecure.h>

static Led ledGreen = Led(PIN_LED_GREEN);
static Led ledRed = Led(PIN_LED_RED);
SonarImpl sonar = SonarImpl(PIN_SONAR_TRIG, PIN_SONAR_ECHO);

static WiFiClientSecure esp_client;
PubSubClient mqtt_client(esp_client);

// MQTT Broker settings
static const char *mqtt_broker = "broker.emqx.io";
static const char *mqtt_username = "SmartRiverMonitoringSystem";
static const char *mqtt_password = "GtYu673Rt";
static const int mqtt_port = 8883;

const char *mqtt_topic_period = "SmartRiverMonitoringSystem/WaterLevelMonitoring/Period";
const char *mqtt_topic_water_level = "SmartRiverMonitoringSystem/WaterLevelMonitoring/WaterLevel";

long unsigned period;

// Root CA Certificate
// Load DigiCert Global Root G2, which is used by EMQX Public Broker: broker.emqx.io
const char *ca_cert = R"(
-----BEGIN CERTIFICATE-----
MIIDjjCCAnagAwIBAgIQAzrx5qcRqaC7KGSxHQn65TANBgkqhkiG9w0BAQsFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBH
MjAeFw0xMzA4MDExMjAwMDBaFw0zODAxMTUxMjAwMDBaMGExCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IEcyMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuzfNNNx7a8myaJCtSnX/RrohCgiN9RlUyfuI
2/Ou8jqJkTx65qsGGmvPrC3oXgkkRLpimn7Wo6h+4FR1IAWsULecYxpsMNzaHxmx
1x7e/dfgy5SDN67sH0NO3Xss0r0upS/kqbitOtSZpLYl6ZtrAGCSYP9PIUkY92eQ
q2EGnI/yuum06ZIya7XzV+hdG82MHauVBJVJ8zUtluNJbd134/tJS7SsVQepj5Wz
tCO7TG1F8PapspUwtP1MVYwnSlcUfIKdzXOS0xZKBgyMUNGPHgm+F6HmIcr9g+UQ
vIOlCsRnKPZzFBQ9RnbDhxSJITRNrw9FDKZJobq7nMWxM4MphQIDAQABo0IwQDAP
BgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBhjAdBgNVHQ4EFgQUTiJUIBiV
5uNu5g/6+rkS7QYXjzkwDQYJKoZIhvcNAQELBQADggEBAGBnKJRvDkhj6zHd6mcY
1Yl9PMWLSn/pvtsrF9+wX3N3KjITOYFnQoQj8kVnNeyIv/iPsGEMNKSuIEyExtv4
NeF22d+mQrvHRAiGfzZ0JFrabA0UWTW98kndth/Jsw1HKj2ZL7tcu7XUIOGZX1NG
Fdtom/DzMNU+MeKNhJ7jitralj41E6Vf8PlwUHBHQRFXGU7Aj64GxJUTFy8bJZ91
8rGOmaFvE7FBcf6IKshPECBV1/MUReXgRPTqh5Uykw7+U0b6LJ3/iyK5S9kJRaTe
pLiaWN0bfVKfjllDiIGknibVb63dDcY3fe0Dkhvld1927jyNxF1WW6LZZm6zNTfl
MrY=
-----END CERTIFICATE-----
)";

void wifi_setup(const char *ssid, const char *password) {
    delay(10);

    // We start by connecting to a WiFi network
    // To debug, please enable Core Debug Level to Verbose

    Serial.println();
    Serial.print("[WiFi] Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);
    // Auto reconnect is set true as default
    // To set auto connect off, use the following function
    //     WiFi.setAutoReconnect(false);

    // Will try for about 10 seconds (20 x 500 ms)
    int tryDelay = 500;
    int numberOfTries = 20;

    // Wait for the WiFi event
    while (true) {
        switch (WiFi.status()) {
            case WL_NO_SSID_AVAIL: Serial.println("[WiFi] SSID not found"); break;
            case WL_CONNECT_FAILED:
                Serial.print("[WiFi] Failed - WiFi not connected! Reason: ");
                return;
                break;
            case WL_CONNECTION_LOST: Serial.println("[WiFi] Connection was lost"); break;
            case WL_SCAN_COMPLETED: Serial.println("[WiFi] Scan is completed"); break;
            case WL_DISCONNECTED: Serial.println("[WiFi] WiFi is disconnected"); break;
            case WL_CONNECTED:
                Serial.println("[WiFi] WiFi is connected!");
                Serial.print("[WiFi] IP address: ");
                Serial.println(WiFi.localIP());
                return;
                break;
            default:
                Serial.print("[WiFi] WiFi Status: ");
                Serial.println(WiFi.status());
                break;
        }
        delay(tryDelay);

        if (numberOfTries <= 0) {
            Serial.print("[WiFi] Failed to connect to WiFi!");
            // Use disconnect function to force stop trying to connect
            WiFi.disconnect();
            return;
        } else {
            numberOfTries--;
        }
    }
}

void mqtt_connect(void) {
    while (!mqtt_client.connected()) {
        ledGreen.switchOff();
        ledRed.switchOn();
        String client_id = "WaterLevelMonitoring-" + String(random(LONG_MAX), HEX);
        Serial.printf("[MQTT] Connecting to MQTT Broker as %s\n", client_id.c_str());
        if (mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("[MQTT] Connected to MQTT broker");
            mqtt_client.subscribe(mqtt_topic_period);
        } else {
            Serial.print("[MQTT] Failed to connect to MQTT broker, rc=");
            Serial.print(mqtt_client.state());
            Serial.println(", retrying in 5 seconds.");
            delay(5000);
        }
    }
    ledRed.switchOff();
    ledGreen.switchOn();
}

void init_config(const char *wifi_ssid, const char *wifi_password, MQTT_CALLBACK_SIGNATURE) {
    ledRed.switchOn();
    period = DEF_T;
    Serial.begin(BAUD_RATE);
    wifi_setup(wifi_ssid, wifi_password);
    randomSeed(micros());
    esp_client.setCACert(ca_cert);
    mqtt_client.setServer(mqtt_broker, mqtt_port);
    mqtt_client.setKeepAlive(60);
    mqtt_client.setCallback(callback);
}
