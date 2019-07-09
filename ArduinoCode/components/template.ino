
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
  
  /*
   * Pass along the output upstream
   */
  upstreamSerial.print( passData ) ;

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
   * If something was received from upstream
   */
  if( passData.length() > 0 ) {
    
    /*
     * Format of received string can be
     * either ID1;ID1-ID2,
     * or     ID1-ID2,
     * In the latter case, pass along downstream
     * In the former case, further processing required
     */

    /*
     * Firstly find if there is a semicolon
     * and if so where it is
     */
    charIndex = passData.indexOf( ";" ) ;

		// If no found, should be -1
    if(charIndex < 0) {
      // Just pass along the string
      Serial.print(passData)
    } else {

			/* 
       * Pass everything after the semicolon downstream
       * (if the semicolon isn't the last character!)
       */
      if((charIndex+1)<passData.length()) {
	      Serial.print(passData.subString(charIndex+1));
      }

		  /*
		   * Generate a string this unitId-upstream unitId,
		   * to send on to the next component
		   */
		  thisConnection = unitId + String( "-" ) + passData.substring( 0 , charIndex ) + "," ;
      
      /*
       * Per the message specification
       * this unit's id must be added to
       * the start of the string followed
       * by a ; so the next unit downstream
       * knows to whom it is attached
       */
      passData = unitId+";"+thisConnection;
    }
    
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
