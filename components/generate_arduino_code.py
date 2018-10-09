
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
                        "Tx" : 5
                      } ,
                "1" : {
                        "Rx" : 7 ,
                        "Tx" : 8
                      }
              }

#Reset light pin
reset_pin = 13

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
                  "led" : False
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
# To be used in #define directives

definitions = {
                    "baudRate" : str( baud_rate ) ,
                    "transferLatency" : str( transfer_latency ) ,
                    "responseWait" : str( response_wait ) ,
                    "resetLight" : str( reset_pin )
              }

##############################
##############################

import os

#Import template
with open( "template.txt" , "r" ) as template_file :
    template_master = template_file.read()

#For each element
for element in elements :
    print( "Generating code for {}".format( element[ "name" ] ) )

    template = template_master

    #Software serial class definition
    for i in range( element[ "serial"] -1 ) :
        template = "SoftwareSerial upstreamSerial( {} , {} ) ;\n\n".format( "softwareSerialRx{}".format(i) , "softwareSerialTx{}".format(i) ) + template 

    #Add define for unitId
    definitions[ "unitId" ] = element[ "code" ]

    #Add define directives
    for key , value in definitions.items() :
        template = "#define {} {}\n\n".format( key , value ) + template

    #Define directives for software serial ports
    for i in range( element[ "serial" ] - 1 ) :
        for key , value in serial_pins[ str(i) ].items() :
            template = "#define {} {}\n\n".format( "softwareSerial{}{}".format( key , i ) , value ) + template

    #Add include directives
    for include in includes :
        template = "#include <{}.h>\n\n".format( include ) + template

    #Create the folder if required
    if not os.path.exists( element[ "code" ] ) :
        os.mkdir( element[ "code" ] )
                                    
    #Save the template to a file in this folder
    with open( "{}/{}.ino".format( element[ "code" ] , element[ "code" ] ) , "w" ) as code_out :
        code_out.write( template )
    
