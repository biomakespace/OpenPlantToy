
#include <stdio.h>

using namespace std;

#include <SoftwareSerial.h>

#define downstreamSerial        Serial

#define SOFTWARE_SERIAL_TX      2
#define SOFTWARE_SERIAL_RX      3
                                  
#define BAUD_RATE               4800
                                    
#define RESET_LIGHT_PIN         13

#define BUFFER_SIZE             128

#define MESSAGE_TERMINATOR      (byte) ';'

// Create software serial object
SoftwareSerial upstreamSerial(SOFTWARE_SERIAL_RX, SOFTWARE_SERIAL_TX);

// Software buffer class

class RingBuffer {
  private:
    byte* bytes;
    int firstByte;
    int nextByte;
   public:
    RingBuffer();
    void push(byte b);
    bool containsFullMessage();
    String extractMessage();
};

RingBuffer::RingBuffer() {
  firstByte = 0;
  nextByte = 0;
  bytes = new byte[BUFFER_SIZE];
}

void RingBuffer::push(byte b) {
  bytes[nextByte] = b;
  // Move on to next space
  nextByte++;
  if (nextByte == BUFFER_SIZE) {
    nextByte = 0;
  }
  // Increment start if buffer is overflowing
  if (firstByte == nextByte) {
    firstByte++;
    if (firstByte == BUFFER_SIZE) {
      firstByte = 0;
    }
  }
}

bool RingBuffer::containsFullMessage() {
  int i = firstByte;
  while(i != nextByte) {
    if (bytes[i] == MESSAGE_TERMINATOR) {
      // Found a terminator
      return true;
    }
    i++;
    // Cycle if we reach the end of the buffer
    if (i == BUFFER_SIZE) {
      i = 0;
    }
  }
  // Didn't find a terminator
  return false;
}

String RingBuffer::extractMessage() {
  int i = firstByte;
  String message = "";
  while (bytes[i] != MESSAGE_TERMINATOR) {
    message += char(bytes[i]);
    i++;
    // Cycle to start if we reach end of array
    if (i == BUFFER_SIZE) {
      i = 0;
    }
    /*
     * If we reach the end of data without
     * finding a terminator then
     * there is not actually a full message
     */
    if (i == nextByte) {
      return "";
    }
  }
  // Got a message - shift start to throw it away
  firstByte = i+1; // +1 to ignore terminator
  return message;
}

/*
 * End of RingBuffer class
 */

// Declare buffers
RingBuffer *upstreamBuffer;
RingBuffer *downstreamBuffer;

/*
 * Helper methods for shifting
 * from hardware to software
 * serial buffers
 */

void shiftUpstreamBytes() {
  while (upstreamSerial.available() > 0) {
    upstreamBuffer->push(upstreamSerial.read());    
  }
}

void shiftDownstreamBytes() {
  while (downstreamSerial.available() > 0) {
    downstreamBuffer->push(downstreamSerial.read());
  }
}


void setup() {
  // Start serial ports
  Serial.begin(BAUD_RATE);
  while(!Serial) {
    // Wait to serial to start up
  }
  upstreamSerial.begin(BAUD_RATE);
  // Initialise software buffers
  upstreamBuffer = new RingBuffer();
  downstreamBuffer = new RingBuffer();
}

void loop() {
  // put your main code here, to run repeatedly:
  
}
