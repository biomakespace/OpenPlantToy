
#include <stdio.h>

using namespace std;

#include <SoftwareSerial.h>

#define downstreamSerial        Serial

#define SOFTWARE_SERIAL_TX      2
#define SOFTWARE_SERIAL_RX      3
                                  
#define BAUD_RATE               4800

#define RESET_LIGHT_PIN         13

#define MESSAGE_TERMINATOR      ';'

#define POLLING_INTERVAL        1000    // Interval of polling components for connectivity, ms

#define BUFFER_SIZE                 128
#define COMMAND_STORE_SIZE          32    // Buffer to hold last received command
#define RESPONSE_BUFFER_SIZE        128   // Buffer to hold accumulated responses
#define ROOT_BUFFER_SIZE            16    // Buffer to hold name of root component
#define UPSTREAM_MESSAGE_SIZE       16
#define DOWNSTREAM_MESSAGE_SIZE     16

// Set response/request sizes
#define IDENTIFY_REQUEST_LENGTH     12
#define IDENTIFY_RESPONSE_LENGTH    22
#define LATEST_REQUEST_LENGTH       6

// Create software serial object
SoftwareSerial upstreamSerial(SOFTWARE_SERIAL_RX, SOFTWARE_SERIAL_TX);

// Various buffers to store responses, commands, etc
byte *lastReceivedCommand = new byte[COMMAND_STORE_SIZE];
byte *previousResponses = new byte[RESPONSE_BUFFER_SIZE];
byte *currentResponses = new byte[RESPONSE_BUFFER_SIZE];
byte *previousRoot = new byte[ROOT_BUFFER_SIZE];
byte *currentRoot = new byte[ROOT_BUFFER_SIZE];
byte *upstreamMessage = new byte[UPSTREAM_MESSAGE_SIZE];
byte *downstreamMessage = new byte[DOWNSTREAM_MESSAGE_SIZE];
byte lastReceivedCommandPointer;
byte previousResponsesPointer;
byte currentResponsesPointer;
byte previousRootPointer;
byte currentRootPointer;
byte downstreamMessagePointer;
byte upstreamMessagePointer;

// Software serial buffers

byte *upstreamBuffer = new byte[BUFFER_SIZE];
byte *downstreamBuffer = new byte[BUFFER_SIZE];
byte upstreamBufferPointer;
byte downstreamBufferPointer;

/*
 * Helper methods for dealing
 * with software serial buffers
 */

void shiftUpstreamBytes() {
  while (upstreamSerial.available() > 0) {
    if (upstreamBufferPointer < BUFFER_SIZE) {
      upstreamBuffer[upstreamBufferPointer] = upstreamSerial.read();
      upstreamBufferPointer++;
    } else {
      upstreamBufferPointer = 0;
      upstreamBuffer[upstreamBufferPointer] = upstreamSerial.read();
    }
  }
}

void shiftDownstreamBytes() {
  while (downstreamSerial.available() > 0) {
    if (downstreamBufferPointer < BUFFER_SIZE) {
      downstreamBuffer[downstreamBufferPointer] = downstreamSerial.read();
      downstreamBufferPointer++;
    } else {
      downstreamBufferPointer = 0;
      downstreamBuffer[downstreamBufferPointer] = downstreamSerial.read();
    }
  }
}

bool upstreamMessageWaiting() {
  for (byte i = 0; i < upstreamBufferPointer; i++) {
    if (upstreamBuffer[i] == MESSAGE_TERMINATOR) {
      return true;
    }
  }
  return false;
}

bool downstreamMessageWaiting() {
  for (byte i = 0; i < downstreamBufferPointer; i++) {
    if (downstreamBuffer[i] == MESSAGE_TERMINATOR) {
      return true;
    }
  }
  return false;
}

void extractUpstreamMessage() {
  byte messageSize = 0;
  while (
    (upstreamBuffer[messageSize] != MESSAGE_TERMINATOR)
    && (messageSize < BUFFER_SIZE)
  ) {
    messageSize++;
  }
  for (byte i = 0; i < messageSize; i++) {
    upstreamMessage[i] = upstreamBuffer[i];
  }
  upstreamMessagePointer = messageSize;
  for (byte i = messageSize + 1; i < BUFFER_SIZE; i++) {
    upstreamBuffer[i-messageSize-1] = upstreamBuffer[i];
  }
  for (byte i = BUFFER_SIZE; i > BUFFER_SIZE - messageSize; i--) {
    upstreamBuffer[i] = 0;
  }
  if (BUFFER_SIZE == messageSize) {
    upstreamBuffer[0] = 0;
  }
  upstreamBufferPointer = upstreamBufferPointer - messageSize - 1;
}

void extractDownstreamMessage() {
  byte messageSize = 0;
  while (
    (downstreamBuffer[messageSize] != MESSAGE_TERMINATOR)
    && (messageSize < BUFFER_SIZE)
  ) {
    messageSize++;
  }
  for (byte i = 0; i < messageSize; i++) {
    downstreamMessage[i] = downstreamBuffer[i];
  }
  downstreamMessagePointer = messageSize;
  for (byte i = messageSize + 1; i < BUFFER_SIZE; i++) {
    downstreamBuffer[i-messageSize-1] = downstreamBuffer[i];
  }
  for (byte i = BUFFER_SIZE; i > BUFFER_SIZE - messageSize; i--) {
    downstreamBuffer[i] = 0;
  }
  if (BUFFER_SIZE == messageSize) {
    downstreamBuffer[0] = 0;
  }
  downstreamBufferPointer = downstreamBufferPointer - messageSize - 1;
}

/*
 * Helper methods to manage responses
 * to incoming messages
 */

void sendCommandUpstream() {
  for (byte i = 0; i < lastReceivedCommandPointer; i++) {
    upstreamSerial.write(lastReceivedCommand[i]);
  }
  // Remember to send stop byte
  upstreamSerial.write(";");
}

/*
 * Helper methods to manage polling 
 * of components for connectivity
 */

// Time of last polling
unsigned long lastPollingTime = millis();

bool pollingDue() {
  return (millis() - lastPollingTime) > POLLING_INTERVAL;
}

void pollComponents() {
  // Save existing responses as 'previous', reset current
  for (byte i = 0; i < ROOT_BUFFER_SIZE; i++) {
    previousRoot[i] = currentRoot[i];
    currentRoot[i] = 0;
  }
  for (byte i = 0; i < RESPONSE_BUFFER_SIZE; i++) {
    previousResponses[i] = currentResponses[i];
    currentResponses[i] = 0;
  }
  // Transfer pointers
  previousRootPointer = currentRootPointer;
  currentRootPointer = 0;
  previousResponsesPointer = currentResponsesPointer;
  currentResponsesPointer = 0;
  // Pass command to components (will automatically trigger response)
  sendCommandUpstream();
  // Update last polling time
  lastPollingTime = millis();
}

/*
 * Helper methods to handle
 * full messages received
 * from both up and downstream
 */

// Wraps the circuit information in JSON for the response
void sendCircuitInformation() {
  downstreamSerial.write('{');
  downstreamSerial.write('"');
  downstreamSerial.write('r');
  downstreamSerial.write('o');
  downstreamSerial.write('o');
  downstreamSerial.write('t');
  downstreamSerial.write('"');
  downstreamSerial.write(':');
  downstreamSerial.write('"');
  for (byte i = 0; i < previousRootPointer; i++) {
    downstreamSerial.write(previousRoot[i]);
  }
  downstreamSerial.write('"');
  downstreamSerial.write(',');
  downstreamSerial.write('"');
  downstreamSerial.write('c');
  downstreamSerial.write('o');
  downstreamSerial.write('n');
  downstreamSerial.write('n');
  downstreamSerial.write('e');
  downstreamSerial.write('c');
  downstreamSerial.write('t');
  downstreamSerial.write('i');
  downstreamSerial.write('o');
  downstreamSerial.write('n');
  downstreamSerial.write('s');
  downstreamSerial.write('"');
  downstreamSerial.write(':');
  downstreamSerial.write('[');
  for (byte i = 0; i < previousResponsesPointer; i++) {
    downstreamSerial.write(previousResponses[i]);    
  }
  downstreamSerial.write(']');
  downstreamSerial.write('}');
  downstreamSerial.write(';');
}

void initialiseBuffers() {
  for (byte i = 0; i < BUFFER_SIZE; i++) {
    upstreamBuffer[i] = 0;
  }
  for (byte i = 0; i < BUFFER_SIZE; i++) {
    downstreamBuffer[i] = 0;
  }
  for (byte i = 0; i < COMMAND_STORE_SIZE; i++) {
    lastReceivedCommand[i] = 0;
  }
  for (byte i = 0; i < RESPONSE_BUFFER_SIZE; i++) {
    previousResponses[i] = 0;
  }
  for (byte i = 0; i < RESPONSE_BUFFER_SIZE; i++) {
    currentResponses[i] = 0;
  }
  for (byte i = 0; i < ROOT_BUFFER_SIZE; i++) {
    previousRoot[i] = 0;
  } 
  for (byte i = 0; i < ROOT_BUFFER_SIZE; i++) {
    currentRoot[i] = 0;
  }  
  for (byte i = 0; i < DOWNSTREAM_MESSAGE_SIZE; i++) {
    downstreamMessage[i] = 0;
  }  
  for (byte i = 0; i < UPSTREAM_MESSAGE_SIZE; i++) {
    upstreamMessage[i] = 0;
  }  
  upstreamBufferPointer = 0;
  downstreamBufferPointer = 0;
  lastReceivedCommandPointer = 0;
  previousResponsesPointer = 0;
  currentResponsesPointer = 0;
  previousRootPointer = 0;
  currentRootPointer = 0;
  downstreamMessagePointer = 0;
  upstreamMessagePointer = 0;
}

byte *identifyRequest = new byte[IDENTIFY_REQUEST_LENGTH];
byte *identifyResponse = new byte[IDENTIFY_RESPONSE_LENGTH];
byte *latestRequest = new byte[LATEST_REQUEST_LENGTH];

void setupFixedDownstreamMessages() {
  identifyRequest[0] = 'W';
  identifyRequest[1] = 'H';
  identifyRequest[2] = 'O';
  identifyRequest[3] = 'G';
  identifyRequest[4] = 'O';
  identifyRequest[5] = 'E';
  identifyRequest[6] = 'S';
  identifyRequest[7] = 'T';
  identifyRequest[8] = 'H';
  identifyRequest[9] = 'E';
  identifyRequest[10] = 'R';
  identifyRequest[11] = 'E';
  identifyResponse[0] = '{';
  identifyResponse[1] = '"';
  identifyResponse[2] = 'm';
  identifyResponse[3] = 's';
  identifyResponse[4] = 'g';
  identifyResponse[5] = '"';
  identifyResponse[6] = ':';
  identifyResponse[7] = '"';
  identifyResponse[8] = 'O';
  identifyResponse[9] = 'P';
  identifyResponse[10] = 'E';
  identifyResponse[11] = 'N';
  identifyResponse[12] = 'P';
  identifyResponse[13] = 'L';
  identifyResponse[14] = 'A';
  identifyResponse[15] = 'N';
  identifyResponse[16] = 'T';
  identifyResponse[17] = 'T';
  identifyResponse[18] = 'O';
  identifyResponse[19] = 'Y';
  identifyResponse[20] = '"';
  identifyResponse[21] = '}';
  latestRequest[0] = 'L';
  latestRequest[1] = 'A';
  latestRequest[2] = 'T';
  latestRequest[3] = 'E';
  latestRequest[4] = 'S';
  latestRequest[5] = 'T';
}

void handleDownstreamMessage() {
  extractDownstreamMessage();
  if (downstreamMessagePointer > 0) {
    // Handle requests to identify unit
    bool isMessageType = true;
    for (byte i = 0; i < IDENTIFY_REQUEST_LENGTH; i++) {
      if (downstreamMessage[i] != identifyRequest[i]) {
        isMessageType = false;
        break;
      }
    }
    if (isMessageType) {
      for (byte i = 0; i < IDENTIFY_RESPONSE_LENGTH; i++) {
        downstreamSerial.write(identifyResponse[i]);
      }
      downstreamSerial.write(';');
      return;
    }

    isMessageType = true;
    // Handle requests to get the latest responses
    for (byte i = 0; i < LATEST_REQUEST_LENGTH; i++) {
      if (downstreamMessage[i] != latestRequest[i]) {
        isMessageType = false;
        break;
      }
    }
    if (isMessageType) {
      sendCircuitInformation();
      return;
    }

    // Assume anything else is a command for the components
    lastReceivedCommandPointer = 0;
    for (byte i = 0; i < downstreamMessagePointer; i++) {
      lastReceivedCommand[lastReceivedCommandPointer] = downstreamMessage[i];
      lastReceivedCommandPointer++;
    }
    
  }
}

void primeCommand() {
  lastReceivedCommand[0] = ';';
  lastReceivedCommandPointer++;
}

void setup() {
  
  // Start serial ports
  downstreamSerial.begin(BAUD_RATE);
  while(!downstreamSerial) {
    // Wait for serial to start up
  }
  upstreamSerial.begin(BAUD_RATE);

  // Initialise software buffers
  initialiseBuffers();

  // Setup fixed messages
  setupFixedDownstreamMessages();

  // Trivial command message, to prompt response
  primeCommand();
}

void loop() {

  // Handle serial in
  shiftUpstreamBytes();
  shiftDownstreamBytes();
  
  // Handle messages from main controller
  if (downstreamMessageWaiting()) {
    handleDownstreamMessage();
  }

  // Handle messages from components
  while (upstreamMessageWaiting()) {
    extractUpstreamMessage();
    bool isConnectionMessage = false;
    for (byte i = 0; i < upstreamMessagePointer; i++) {
      if (upstreamMessage[i] == '-') {
        isConnectionMessage = true;
      }
    }
    if (!isConnectionMessage) {
      for (byte i = 0; i < upstreamMessagePointer; i++) {
        currentRoot[i] = upstreamMessage[i];
        currentRootPointer++;
      }
    } else {
      // 2. IDx-IDy -> has dash, connection, add to responses
      if (currentResponsesPointer > 0) {
        // Preface with comma if there is already something in the string
        currentResponses[currentResponsesPointer] = ',';
        currentResponsesPointer++;
      }
      currentResponses[currentResponsesPointer] = '"';
      currentResponsesPointer++;
      for (byte i = 0; i < upstreamMessagePointer; i++) {
        currentResponses[currentResponsesPointer] = upstreamMessage[i];
        currentResponsesPointer++;
      }
      currentResponses[currentResponsesPointer] = '"';
      currentResponsesPointer++;
    }
  }

  // Check if a new polling message is due
  if (pollingDue()) {
    pollComponents();
  }
  
}
