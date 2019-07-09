#include <SoftwareSerial.h>

#define softwareSerialTx0 5
#define softwareSerialRx0 4
#define unitId "5UT"

#define ledPin 6

#define resetLight 13

#define responseWait 1000

#define transferLatency 5

#define baudRate 4800

int waitCounter ;
bool isUpstream ;
bool confirmReceived ;
String thisConnection ;
String passData ;
int charIndex ;
SoftwareSerial upstreamSerial( softwareSerialRx0 , softwareSerialTx0 ) ;


void setup() {

  /* 
   *  Open serial communication 
   *  between nano and downstream source
   */
  Serial.begin( baudRate ) ;
  
  while( !Serial ) {
    ; //Pass
  }
  
  /*
   * Open serial communication
   * between nano and upstream source
   */
  upstreamSerial.begin( baudRate ) ;
  
}

void loop() {
  
  /*
   * Read input from downstream
   */
  passData = "" ;
  
  while( Serial.available() > 0 ) {
    
    //Toggle the reset light while reading
    //to show that the nano is doing something
    digitalWrite( resetLight, HIGH ) ;
    
    passData = passData + char( Serial.read() ) ;
    
    //Account for latency in transfer
    delay( transferLatency ) ;
    
    digitalWrite( resetLight , LOW ) ;
  }
  
  /*
   * Any actions that are sent from
   * the controller unit are taken here
   * such as switching on lights, etc
   * to show if the circuit is (in)correct
   */
  
  //Below replaced with led switching code, if applicable
  //<LED>

  if(passData.length()>0) { 
    /*
     * Pass along the output upstream
     */
    upstreamSerial.print( passData ) ;
    /*
     * Pass own unit id downstream
     */
    Serial.print(unitId+String(";"));
  }

  /*
   * Get message from upstream, if it exists
   */
  passData = "" ;
  while( upstreamSerial.available() > 0 ) {
    
    //Toggle the reset light while reading
    //to show that the nano is doing something
    digitalWrite( resetLight, HIGH ) ;
    
    passData = passData + char( upstreamSerial.read() ) ;
    
    //Account for latency in transfer
    delay( transferLatency ) ;
    
    digitalWrite( resetLight , LOW ) ;
  }
  
  /*
   * If something was received from upstream
   */
  if( passData.length() > 0 ) {
    
    /*
     * Format of received string can be
     * either ID1;
     * or     ID1-ID2,
     * In the latter case, just pass along downstream
     * In the former case, construct new string
     */

    /*
     * Firstly find if there is a semicolon
     * and if so where it is
     */
    charIndex = passData.indexOf( ";" ) ;

    // If not found, should be -1
    if(charIndex < 0) {
      // Just pass along the string
      Serial.print(passData);
    } else {
      // Generate a string this unitId-upstream unitId,
      thisConnection = unitId + String( "-" ) + passData.substring( 0 , charIndex ) + "," ;
      // Pass that string downstream
      Serial.print(thisConnection);
    }
    
  }

}
