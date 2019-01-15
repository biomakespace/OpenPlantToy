
#Needed for serial communication
#with the base unit
import serial

#Converts a list of connections
#as a string of the following format
# id1-id2,id2-id3,id2-id4,id4-id5
#to an array of connected pairs
#in the following format
# [ [ id1 , id2 ] , [ id2 , id3 ] , [ id2 , id4 ] , [ id4 , id5 ] ]
def parse_tree( tree_in ) :
    #Copy the input string
    #because it will be changed
    tree = tree_in
    #This will be the array of connections
    connections = []
    #So long as there is a comma
    #in the string, indicating that
    #there is another connection
    #to be parsed
    while "," in tree :
        #Split the string at the commas
        #and grab the first substring
        #format id1-id2
        first_connection = tree.split(",")[0]
        #Split this at the - character to get
        #an array format [ id1 , id2 ]
        first_connection = first_connection.split( "-" )
        #Add this connection to the list
        connections.append( first_connection )
        #Cut out the first connection in the
        #string, including the comma
        tree = tree[ tree.find( "," )+1 : ]
    return connections



#Checks two sets of connections
#in the array format
# [ [ id1 , id2 ] , [ id2 , id3 ] , [ id2 , id4 ] , [ id4 , id5 ] ]
#to see if each connection in
#each set has a corresponding
#connection in the other set
#
### Note that this will currently fail
### in the following case
### tree_1 = [ [ 1 , 2 ] , [ 1 , 2 ] ]
### tree_2 = [ [ 1 , 2 ] , [ 1 , 3 ] ]
### because both entries in tree_1
### will match with the first entry in tree_2
#
def tree_match( tree_1 , tree_2 ) :
    
    #Start by assuming that they
    #do match, then try to find a
    #connection that has no match
    is_match = True

    #If either of the two input
    #arrays is empty, report no match
    is_match = not ( ( len( tree_1 ) == 0 ) or ( len( tree_2 ) == 0 ) )

    #If the arrays do not match in length
    #then they cannot match
    is_match = len( tree_1 ) == len( tree_2 )

    #If it has already been demonstrated
    #that the arrays do not match, no
    #need to test connection by connection
    if is_match :
        
        #For each connection in one of the sets
        for connection_1 in tree_1 :
            
            #Assume there is no match
            #in the other set
            this_match = False

            #Then check it against all connections
            #in the other set for a match
            for connection_2 in tree_2 :
                
                #The first and second entries of
                #the connection both have to match
                #Can't match first of one with
                #second of the other
                # i.e. [ 1 , 2 ] == [ 1 , 2 ]
                # but  [ 1 , 2 ] != [ 2 , 1 ]
                #order of connections is important
                if( ( connection_1[0] == connection_2[0] ) and ( connection_1[1] == connection_2[1] ) ) :
                    this_match = True
                    
            #Since every single connection
            #needs to find a match
            #"and" them all together
            is_match = is_match and this_match
            
    return is_match



# Inertia + 1 = number of incorrect responses before turning off the light
inertia = 2

serial1 = serial.Serial( "/dev/ttyUSB0" , 4800 , timeout=1 )
#serial2 = serial.Serial( "/dev/ttyUSB1" , 4800 , timeout=3 )
print( serial1.name )

correct_circuit = [
                    [ "TRM" , "3UT" ] ,
                    [ "3UT" , "FRT" ] ,
                    [ "FRT" , "5UT" ] ,
                    [ "5UT" , "PRM" ] ,
                    [ "PRM" , "REP" ] #,
                    #[ "REP" , "DRP" ]
                  ] 

response = "REP,OFF;"

#Count how many incorrect responses we've had since last correct one
incorrect = 0

while True :
    #Try to read in the response
    try :
        characters = serial1.read(50).decode( "utf-8" )
        #If it fails, assume empty response
    except UnicodeDecodeError :
        characters = ""
    #Print response
    print( "Raw response:" , characters )
    if( ";" in characters ) :
        characters = characters.split( ";" ).pop()
        print( "Remove last device name: " , characters )
    print( response )
    print( response.encode( "ascii" ) )
    serial1.write( response.encode( "ascii" ) )
    try :
        connections = parse_tree( characters )
        print( "Pairwise connections:" , connections )
        if( tree_match( connections , correct_circuit ) ) :
            incorrect = 0
            print( "MATCH" )
            response = "TRM,ON;"
        else :
            incorrect += 1
            print( "NO MATCH" )
            if incorrect > inertia :
                response = "TRM,OFF;"
    except Exception as e :
        pass
    print( "###############" )
    
