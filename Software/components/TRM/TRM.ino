#include <SoftwareSerial.h>

#define softwareSerialTx0 3
#define softwareSerialRx0 4
#define unitId "TRM"

#define ledPin 2

#define resetLight 13

#define responseWait 1000

#define transferLatency 5

#define baudRate 4800

String directives ;
String directive ;
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

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  
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
    //Copy the data in
  directives = passData ;
  
  while( directives.indexOf( ";" ) > 0 ) { // 1

    //Find the first occurence of ";" in directives
    charIndex = directives.indexOf( ";" ) ;

    //While there is still ";" in directives
    if( charIndex > 0 ) { // 2

      //Get the first directive in the string
      directive = directives.substring( 0 , charIndex ) ;

      //If that directive contains this unit's id
      if( directive.indexOf( unitId ) >= 0 ) { // 3

        //If the directive is to turn on the light, turn it on
        if( directive.indexOf( "ON" ) > 0 ) { // 4
          digitalWrite( ledPin , HIGH ) ;
        } else {  // 4
          //Otherwise, ensure that the light is off
          digitalWrite( ledPin , LOW ) ;
        } // 4

      } // 3
      
    } // 2

    //Chop off the first directive, because it has been checked
    directives = directives.substring( charIndex ) ;

  } // 1


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
  if(passData.length() > 0) {
    
    /*
     * Format of received string can be
     * either ID1;
     * or     ID1-ID2;
     * In the latter case, just pass along downstream
     * In the former case, construct new string
     */

    /*
     * Firstly find if there is a hyphen
     * and if so where it is
     * Messages of format ID1-ID2; will have
     * messages of format ID1; will not
     */
    charIndex = passData.indexOf("-");

    // If not found, should be -1
    if(charIndex >= 0) {
      // Just pass along the message ID1-ID2
      Serial.print(passData);
    } else {
      // Generate a string this unitId-upstream unitId,
      thisConnection = unitId + String("-") + passData.substring(0, charIndex); // + ";";
      // Pass that string downstream
      Serial.print(thisConnection);
    }
    
  }

}
