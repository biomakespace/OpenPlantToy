
void setup() {
  
  /*
   * Assume initially that something is upstream
   */
  isUpstream = true ;

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
    * Wait for response
    * only if we think something is attached upstream
    */
   waitCounter = 0 ;
   while( !upstreamSerial.available() & isUpstream & ( waitCounter < responseWait ) ) {
     delay( 1 ) ;
     waitCounter++ ;
   }
 
   // If nothing received
   if( !upstreamSerial.available() ) {
     // Assume nothing is connected upstream
     isUpstream = false ;
   } else {
     /* 
      * If something received
      * something is connected upstream 
      */
     isUpstream = true ;
   }

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
