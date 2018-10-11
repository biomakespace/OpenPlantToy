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
