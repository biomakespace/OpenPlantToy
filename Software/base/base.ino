
#include <SoftwareSerial.h>

#define SOFTWARE_SERIAL_TX 2
#define SOFTWARE_SERIAL_RX 3

#define BAUD_RATE 4800

#define RESET_LIGHT_PIN 13

// Create software serial object
SoftwareSerial upstreamSerial(SOFTWARE_SERIAL_RX, SOFTWARE_SERIAL_TX);
void setup() {
  Serial.begin(BAUD_RATE);
  while(!Serial) {
    // Wait to serial to start up
  }
  upstreamSerial.begin(BAUD_RATE);
}

void loop() {
  // put your main code here, to run repeatedly:

}
