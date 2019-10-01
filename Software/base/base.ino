
#include <SoftwareSerial.h>

#define SOFTWARE_SERIAL_TX      2
#define SOFTWARE_SERIAL_RX      3
                                  
#define BAUD_RATE               4800
                                    
#define RESET_LIGHT_PIN         13

#define BUFFER_SIZE             128

// Create software serial object
SoftwareSerial upstreamSerial(SOFTWARE_SERIAL_RX, SOFTWARE_SERIAL_TX);

// Buffers for serial in
String upstreamBuffer = "";     // Upstream -> away from computer
String downstreamBuffer = "";   // Downstream <- towards computer

void setup() {
  // Reserve space for the buffers
  upstreamBuffer.reserve(BUFFER_SIZE);
  downstreamBuffer.reserve(BUFFER_SIZE);
  Serial.begin(BAUD_RATE);
  while(!Serial) {
    // Wait to serial to start up
  }
  upstreamSerial.begin(BAUD_RATE);
}

void moveUpstreamBytesToBuffer() {
  while(Serial.available() > 0) {
    if (downstreamBuffer.length() < BUFFER_SIZE) {
      downstreamBuffer += char(Serial.read());
    }
  }
}

void moveDownstreamBytesToBuffer() {
  while(upstreamSerial.available() > 0) {
    if (upstreamBuffer.length() < BUFFER_SIZE) {
      upstreamBuffer += char(Serial.read());
    }
  }  
}

void loop() {
  // put your main code here, to run repeatedly:

}
