
#include <SoftwareSerial.h>

int charIndex ;
String passData = "" ;
String unitId = "REP" ;
String thisConnection ;
String directives ;
String directive ;
bool confirmReceived ;
int inertia ;

/*
 * 4 (D4) is Rx
 * 5 (D5) is Tx
 */
SoftwareSerial upstreamSerial( 4 , 5 ) ;

void setup() {
  /* 
   *  Open serial communication 
   *  between nano and downstream source
   */
  Serial.begin( 4800 ) ;
  while( !Serial ) {
    ; //Pass
  }
  upstreamSerial.begin( 4800 ) ;
  Serial.print( "Opened downstream communications" ) ;
  upstreamSerial.print( "Opened upstream communications" ) ;
  //Debug
  pinMode( 6 , OUTPUT ) ;
  digitalWrite( 6 , LOW ) ;
}

void loop() {
  /*
   * Wait for input from downstream
   */
  //while( Serial.available() == 0 ) {
  //  ; //Pass
  //}

  delay( 500 ) ;
  
  /*
   * Read input from downstream
   */
  passData = "" ;
  while( Serial.available() > 0 ) {
    digitalWrite( 13, HIGH ) ;
    passData = passData + char( Serial.read() ) ;
    //Account for latency in transfer
    delay(5) ;
    digitalWrite( 13 , LOW ) ;
  }
  
  /*
   * Confirm receipt
   */
  //Serial.print( "200" ) ;
  
  /*
   * Do anything, like turning on LEDs
   */

  //Copy the data in
  directives = passData ;
  if( directives.equals( "" ) and inertia > 3 ) {
    digitalWrite( 6 , LOW ) ;
  }
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
          digitalWrite( 6 , HIGH ) ;
        } else {  // 4
          //Otherwise, ensure that the light is off
          digitalWrite( 6 , LOW ) ;
        } // 4
      } // 3
      
    } // 2
    //Chop off the first directive, because it has been checked
    directives = directives.substring( charIndex ) ;
  } // 1
  
  /*
   * Pass along output upstream
   */
  upstreamSerial.print( passData ) ;
  
  /*
   * Wait for confirmation of receipt
   */
  delay( 500 ) ;

  /*
   * Get reply, if it exists
   */
  passData = "" ;
  while( upstreamSerial.available() > 0 ) {
    digitalWrite( 13, HIGH ) ;
    passData = passData + char( upstreamSerial.read() ) ;
    digitalWrite( 13 , LOW ) ;
  }
  
  /*
   * If something upstream confirms receipt
   */
  if( passData.length() > 0 ) {
    //We got data this time
    inertia = 0 ;
    //Throw away response
    //passData = passData.substring(3) ;
    //Split off sending unitId
    charIndex = passData.indexOf( ";" ) ;
    //Add connection to send of string
    thisConnection = unitId + "-" + passData.substring( 0 , charIndex ) ;
    //Add this unitId to start of string
    passData = unitId + passData.substring( charIndex ) + thisConnection + "," ; 
  } else {
    /*
     * No reply, we are furthest in chain from base
     */
     passData = unitId + ";" ;
     inertia = inertia + 1 ;
  }
  /*
   * Pass back downstream the required data
   */
  Serial.print( passData ) ;

}
