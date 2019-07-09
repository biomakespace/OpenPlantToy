
#Needed for serial communication
#with the base unit
import serial
import datetime

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



def milliseconds_elapsed_since(initial_time):
    time_difference = datetime.datetime.now() - initial_time
    return (time_difference.seconds/1000.0) + (time_difference.microseconds()*1000)

# inertia + 1 = number of incorrect responses before turning off the light
inertia = 2

# Open the serial port on which the circuit component is connected
serial1 = serial.Serial( "/dev/ttyUSB0" , 4800 , timeout=1 )
#serial2 = serial.Serial( "/dev/ttyUSB1" , 4800 , timeout=3 )
# Print the name of the serial port, debug information
print( serial1.name )

# The internal circuit representation of the
# circuit which is "correct"
correct_circuit = [
                    [ "TRM" , "3UT" ] ,
                    [ "3UT" , "FRT" ] ,
                    [ "FRT" , "5UT" ] ,
                    [ "5UT" , "PRM" ] ,
                    [ "PRM" , "REP" ] #,
                    #[ "REP" , "DRP" ]
                  ] 

# Initial message to circuit, assuming incorrect circuit
response = "TRM,OFF;"

# Count how many incorrect responses we've had since last correct one
incorrect = 0

# How long to wait for responses in milliseconds
RESPONSE_WAIT_TIMEOUT = 1000

# Forever (until broken)
while True :
    
    # New logic
    
    # Send something out
    try:
        serial1.write(response.encode('ascii'))
    except:
        # Break & quit if connection lost
        print("Serial connection seems to be lost, stopping")
        break
    
    # Store parsed connections here
    assembled_circuit = []
    # Wait a while to get a bunch of responses
    start_time = datetime.datetime.now()
    while(milliseconds_elapsed_since(start_time)<RESPONSE_WAIT_TIMEOUT):
        pass

    # Get any received response, and decode from bytes to string
    received = serial1.read(50).decode("ascii")
    # Split by ,
    messages = received.split(",")
    # Split by any ;, append results to array
    for message in messages:
        messages = messages + message.split(";")
    # Throw out anything with ; in it
    messages = [m for m in message if ";" not in m]
    # Throw out anything without a dash
    messages = [m for m in message if "-" in m]
    # --- Add those responses into a circuit representation as received
    # Split the messages by the dash ID1-ID2
    # yielding connections in format [ID1,ID2]
    for message in messages:
        assembled_circuit.append(message.split("-"))        

    
    # Check against correct representation
    # Update response based on this
        
    # Print response, debug information
    print( "From circuit:" , assembled_circuit )

    # I think the main point of failure would be
    # the first line, the call to parse_tree, if
    # the string reported by the circuit is not well formed
    # Potentially the tree_match call could produce an error
    # if one of the arrays of connections is ill-formed
    # but this should either be very unlikely to happen
    # or happen every time if the "correct" circuit
    # is not set up correctly at the start
    try :

        # Check if reported circuit matches correct circuit
        if( tree_match( assembled_circuit , correct_circuit ) ) :

            # If so reset number of incorrect circuits reported
            incorrect = 0

            # Confirm match, debug information
            print( "MATCH" )

            # Set response for correct circuit
            response = "TRM,ON;"

        # If reported circuit does not match the correct circuit
        else :

            # Increment number of incorrect responses seen
            incorrect += 1

            # Report lack of match, debug information
            print( "NO MATCH" )

            # If there have been too many incorrect responses,
            # set the response for an incorrect circuit
            if incorrect > inertia :
                response = "TRM,OFF;"

    # Catch all exceptions and do nothing with them, for now
    # To be improved in the future
    # Note that this means that the response sent to the circuit on
    # the next iteration of the loop, will be the same as the one
    # send earlier in this iteration
    except Exception as e :
        pass

    # Separator between loops, for better legibility of debug information
    print( "###############" )
    
