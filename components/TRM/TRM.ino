#include <SoftwareSerial.h>

#define softwareSerialRx0 4
#define softwareSerialTx0 5
#define transferLatency 5

#define responseWait 1000

#define unitId "TRM"

#define resetLight 13

#define baudRate 4800

#define ledPin 6

String directives ;
String directive ;
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
   * Wait for input from downstream
   * This should always come if the object is part of the circuit
   */
  while( Serial.available() == 0 ) {
    ; //Pass
  }
  
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

  
  /*
   * Pass along the output upstream
   */
  upstreamSerial.print( passData ) ;
  
  /*
   * Wait for confirmation of receipt
   */
  delay( responseWait ) ;

  /*
   * Get reply, if it exists
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
   * If something upstream confirms receipt
   */
  if( passData.length() > 0 ) {
    
    /*
     * Format of received string should be
     * upstream unitId;connections in format 1-2,2-3, ... ,
     */
     
    /*
     * Firstly split off everything up to
     * the semicolon, to get the upstream unitId
     */
    charIndex = passData.indexOf( ";" ) ;
    
    /*
     * Generate a string this unitId-upstream unitId
     * to add to the list of connections
     */
    thisConnection = unitId + String( "-" ) + passData.substring( 0 , charIndex ) ;
    
    /*
     * Add this unitId to the start of the string
     * Note that the semicolon required between
     * this unitId and the list of connections
     * is the first character of 
     * passData.substring( charIndex )
     */
    passData = unitId + passData.substring( charIndex ) + thisConnection + "," ; 
    
  } else {
    
    /*
     * This unit didn't receive any input from upstream
     * so it should assume that it is furthest from
     * the base in this part of the tree
     */
     passData = unitId + String( ";" ) ;
     
  }
  
  /*
   * The generated sting is then communicated downwards
   * to trickle down to the base unit
   */
  Serial.print( passData ) ;

}
