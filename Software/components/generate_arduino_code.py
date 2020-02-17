
##############################
##############################
# Configuration Options

#Headers
includes = [
                "SoftwareSerial"
           ]

#Software serial port pins
serial_pins = {
                "0" : {
                        "Rx" : 4 ,
                        "Tx" : 3
                      } ,
                "1" : {
                        "Rx" : 7 ,
                        "Tx" : 8
                      }
              }

#Reset light pin
reset_pin = 13

#LED light pin
led_pin = 2

#Baud rate
baud_rate = 4800

#Transfer latency delay (ms)
transfer_latency = 5

#Response wait time (ms)
response_wait = 1000

##############################
# Circuit elements

elements = [
              {
                  "name" : "Terminator" ,
                  "code" : "TRM" ,
                  "serial" : 2 ,
                  "led" : True
              } ,
              {
                  "name" : "3'UTR" ,
                  "code" : "3UT" ,
                  "serial" : 2 ,
                  "led" : False
              } ,
              {
                  "name" : "5'UTR" ,
                  "code" : "5UT" ,
                  "serial" : 2 ,
                  "led" : False
              } ,
              {
                  "name" : "FRET2" ,
                  "code" : "FRT" ,
                  "serial" : 2 ,
                  "led" : False
              } ,
              {
                  "name" : "Promoter" ,
                  "code" : "PRM" ,
                  "serial" : 2 ,
                  "led" : False
              } ,
              {
                  "name" : "Repressor" ,
                  "code" : "REP" ,
                  "serial" : 2 ,
                  "led" : False
              } ,
              {
                  "name" : "Derepressor" ,
                  "code" : "DRP" ,
                  "serial" : 2 ,
                  "led" : False
              } ,
           ]

##############################
##############################
# Python imports

import os

##############################
##############################
# Importing templates

# Main template
with open( "template.ino" , "r" ) as template_file :
    template_master = template_file.read()

# LED switching code
with open( "led_snippet.ino" , "r" ) as template_file :
    led_code = template_file.read()

##############################
##############################
# To be used in #define directives

definitions = {
                    "baudRate" : str( baud_rate ) ,
                    "transferLatency" : str( transfer_latency ) ,
                    "responseWait" : str( response_wait ) ,
                    "resetLight" : str( reset_pin ) ,
                    "ledPin" : str( led_pin )
              }

##############################
##############################
# Variable declarations

#Always required
required_variables = [
                        {
                            "type" : "int" ,
                            "name" : "charIndex"
                        } ,
                        {
                            "type" : "String" ,
                            "name" : "passData"
                        } ,
                        {
                            "type" : "String" ,
                            "name" : "thisConnection"
                        } ,
                        {
                            "type" : "bool" ,
                            "name" : "confirmReceived"
                        } ,
                        {
                            "type" : "bool" ,
                            "name" : "isUpstream"
                        } ,
                        {
                            "type" : "int" ,
                            "name" : "waitCounter"
                        }
                     ]

#Conditionally required
conditional_variables = {
                            "led" : [
                                        {
                                            "type" : "String" ,
                                            "name" : "directive"
                                        } ,
                                        {
                                            "type" : "String" ,
                                            "name" : "directives"
                                        }
                                    ]
                        }

##############################
##############################
# Tags to be replaced with code

replacements = {
                 "led" : {
                             "tag" : "//<LED>" ,
                             "code" : led_code
                         }
               }

##############################
##############################

#For each element
for element in elements :
    print( "Generating code for {}".format( element[ "name" ] ) )

    template = template_master

    #Software serial class definition
    for i in range( element[ "serial"] -1 ) :
        template = "SoftwareSerial upstreamSerial( {} , {} ) ;\n\n".format( "softwareSerialRx{}".format(i) , "softwareSerialTx{}".format(i) ) + template 

    #Required variable declarations
    for variable in required_variables :
        template = "{} {} ;\n".format( variable[ "type" ] , variable[ "name" ] ) + template

    #Conditional variable declarations
    if element[ "led" ] :
        for variable in conditional_variables[ "led" ] :
            template = "{} {} ;\n".format( variable[ "type" ] , variable[ "name" ] ) + template

    #Add define for unitId
    definitions[ "unitId" ] = "\"" + element[ "code" ] + "\"" 

    #Add define directives
    for key , value in definitions.items() :
        template = "#define {} {}\n\n".format( key , value ) + template

    #Define directives for software serial ports
    for i in range( element[ "serial" ] - 1 ) :
        for key , value in serial_pins[ str(i) ].items() :
            template = "#define {} {}\n".format( "softwareSerial{}{}".format( key , i ) , value ) + template

    #Add include directives
    for include in includes :
        template = "#include <{}.h>\n\n".format( include ) + template

    #Replace any tags with code
    if element[ "led" ] :
        template = template.replace( replacements[ "led" ][ "tag" ] , replacements[ "led" ][ "code" ] )

    #Create the folder if required
    if not os.path.exists( element[ "code" ] ) :
        os.mkdir( element[ "code" ] )
                                    
    #Save the template to a file in this folder
    with open( "{}/{}.ino".format( element[ "code" ] , element[ "code" ] ) , "w" ) as code_out :
        code_out.write( template )
    
