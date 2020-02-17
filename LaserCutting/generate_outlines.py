#!/usr/bin/env python3
# -*- coding: utf-8 -*-

width = 400
height = 800

cut_colour = "#ff0000"
# UPDATE ME
cut_width = 1.0

out_file = "test.svg"

out_string = ""



def path( color , weight , startx , starty , endx , endy ) :
    element = "<path stroke=\"{}\" stroke-width=\"{}\" d=\"M {} {} L {} {}\"/>\n".format( color , weight , startx , starty , endx , endy )
    return element



def init( width , height ) : # mm
    return "<svg width=\"{0}mm\" height=\"{1}mm\" viewBox=\"0 0 {0} {1}\" xmlns=\"http://www.w3.org/2000/svg\">\n".format( width , height )



def close() :
    return "</svg>\n"



def cut_rectangle( start , width , height ) :
    return Rectangle( start , width , height , "none" , cut_colour , cut_width ).draw()
   
                  
                     
def engrave_rectangle( start , width , height , degree ) :
    whiteness = 1.0 - (degree/100.0)
    colour_rgb = whiteness*255
    colour = "#" + "{:02x}".format( int(colour_rgb) )*3
    return Rectangle( start , width , height , colour , "none" , cut_width ).draw()



def layer_engrave_rectangle( start , width , height , degree , layers ) :
    output = ""
    for i in range(layers) :
        output += engrave_rectangle( start , width , height , degree )
    return output



class Rectangle() :
    
    def __init__( self , start , width , height , fill_colour , stroke_colour , stroke_width ):
        self.start = start
        self.width = width
        self.height = height
        self.fill_colour = fill_colour
        self.stroke_colour = stroke_colour
        self.stroke_width = stroke_width
        
    def draw( self ) :
        return "<rect style=\"stroke:{};stroke-width:{};fill:{};\" width=\"{}\" height=\"{}\" x=\"{}\" y=\"{}\"/>\n".format( 
                self.stroke_colour ,
                self.stroke_width ,
                self.fill_colour ,
                self.width ,
                self.height ,
                self.start[0] ,
                self.start[1]
            )



class Circle() :
    
    def __init__( self , x_centre , y_centre , radius , fill_colour , stroke_colour , stroke_width ) :
        self.x_centre = x_centre
        self.y_centre = y_centre
        self.radius = radius
        self.fill_colour = fill_colour
        self.stroke_colour = stroke_colour
        self.stroke_width = stroke_width
        
    def draw( self ) :
        return "<circle style=\"fill:{};stroke:{};stroke-width:{};\" cx=\"{}\" cy=\"{}\" r=\"{}\"/>\n".format(
                self.fill_colour ,
                self.stroke_colour ,
                self.stroke_width ,
                self.x_centre ,
                self.y_centre ,
                self.radius
            )



class CrenellatedLine() :
    
    def __init__( self , start , crenellations , depth , length , colour , weight , horizontal=True , top=True ) :
        self.start = start
        self.crenellations = crenellations
        self.depth = depth
        self.length = length
        self.colour = colour
        self.weight = weight
        self.horizontal = horizontal
        self.top = top
        
    def draw( self ) :
        if self.horizontal :
            return self.draw_horizontal()
        else :
            return self.draw_vertical()
        
    def draw_horizontal( self ) :
        output = ""
        crenellation_length = self.length/(1+(2*self.crenellations))
        x0 = self.start[0]
        y0 = self.start[1] + self.depth
        x1 = x0
        
        i = 0
        
        # Switch between crenellations going 
        # "upward first" and "downward first"
        direction = 2*int( self.top ) - 1
        
        while x1 < (self.length + self.start[0])*0.996 :
            # Horizontal, bottom
            if i % 4 == 0 :
                x1 = x0 + crenellation_length
                y1 = y0
            # Vertical, up
            if i % 4 == 1 :
                x1 = x0
                y1 = y0 + self.depth * direction
            # Horizontal, top
            if i % 4 == 2 :
                x1 = x0 + crenellation_length
                y1 = y0
            # Vertical, down
            if i % 4 == 3 :
                x1 = x0
                y1 = y0 - self.depth * direction
            
            output += path( self.colour , self.weight , x0 , y0 , x1 , y1 )
        
            x0 = x1
            y0 = y1
            i += 1       
            
        return output
    
    def draw_vertical( self ) :
        output = ""
        crenellation_length = self.length/(1+(2*self.crenellations))
        x0 = self.start[0]
        y0 = self.start[1] + self.depth
        y1 = y0
        
        i = 0
        
        # Switch between crenellations going 
        # "upward first" and "downward first"
        direction = 2*int( self.top ) - 1
        
        while y1 < (self.length + self.start[1]) :
            # Vertical, left
            if i % 4 == 0 :
                x1 = x0
                y1 = y0 + crenellation_length
            # Horizontal, right
            if i % 4 == 1 :
                x1 = x0 + self.depth * direction
                y1 = y0 
            # Vertical, right
            if i % 4 == 2 :
                x1 = x0 
                y1 = y0 + crenellation_length
            # Horizontal, left
            if i % 4 == 3 :
                x1 = x0 - self.depth * direction
                y1 = y0 
            
            output += path( self.colour , self.weight , x0 , y0 , x1 , y1 )
        
            x0 = x1
            y0 = y1
            i += 1   

        return output



class CrenellatedSideSpecification() :
    
    def __init__( self , start , length , height , depth ,
                 horizontal_number , vertical_number ,
                 colour , weight , invert
                 ) :
        self.start = start
        self.length = length
        self.height = height
        self.depth = depth
        self.horizontal_number = horizontal_number
        self.vertical_number = vertical_number
        self.colour = colour
        self.weight = weight
        self.invert = invert

    def copy( self ) :
        copy = CrenellatedSideSpecification(
                    self.start ,
                    self.length ,
                    self.height ,
                    self.depth, 
                    self.horizontal_number ,
                    self.vertical_number ,
                    self.colour ,
                    self.weight ,
                    self.invert
                )
        return copy



class CrenellatedSide() :
    
    def __init__( self , specification ) :
        self.specification = specification
        
    def draw( self ) :
        output = ""
        sides = []
        top_left = self.specification.start
        top_right = [ self.specification.start[0] + self.specification.length , self.specification.start[1] ]
        bottom_left = [ self.specification.start[0] , self.specification.start[1] + self.specification.height ]
        # Top
        sides.append( 
                CrenellatedLine( 
                        top_left , 
                        self.specification.horizontal_number , 
                        self.specification.depth , 
                        self.specification.length , 
                        self.specification.colour , 
                        self.specification.weight , 
                        True , 
                        not self.specification.invert[0] 
                        ) 
                )
        # Bottom
        sides.append( 
                CrenellatedLine( 
                        bottom_left , 
                        self.specification.horizontal_number , 
                        self.specification.depth , 
                        self.specification.length , 
                        self.specification.colour , 
                        self.specification.weight , 
                        True , 
                        self.specification.invert[1] 
                        ) 
                )
        # Left
        sides.append( 
                CrenellatedLine( 
                        top_left , 
                        self.specification.vertical_number , 
                        self.specification.depth , 
                        self.specification.height , 
                        self.specification.colour , 
                        self.specification.weight , 
                        False , 
                        not self.specification.invert[2] 
                        ) 
                 )
        #Right
        sides.append( 
                CrenellatedLine( 
                        top_right , 
                        self.specification.vertical_number , 
                        self.specification.depth , 
                        self.specification.height , 
                        self.specification.colour , 
                        self.specification.weight , 
                        False , 
                        self.specification.invert[3] 
                        ) 
                )
        for side in sides :
            output += side.draw()
        return output



class CrenellatedBoxSpecification() :
    
    def __init__( self , start , length , height , depth , 
                 horizontal_number , vertical_number , separation , 
                 connectors , colour , stroke_width ) :
        self.start = start
        self.length = length
        self.height = height
        self.depth = depth
        self.horizontal_number = horizontal_number
        self.vertical_number = vertical_number
        self.separation = separation
        self.connectors = connectors
        self.colour = colour
        self.stroke_width = stroke_width
        
        

class CrenellatedBox() :
    
    def __init__( self , specification ) :
        self.specification = specification

    def get_side_specification( self , side ) :
        
        basis_specification = CrenellatedSideSpecification(
                self.specification.start , 
                self.specification.length , 
                self.specification.height , 
                self.specification.depth , 
                self.specification.horizontal_number , 
                self.specification.vertical_number , 
                self.specification.colour , 
                self.specification.stroke_width , 
                [ False , False , False , False ]
                )
        
        if side == "front" :
            return basis_specification
        
        if side == "back" :
            basis_specification.start = [ self.specification.start[0] ,
                                         self.specification.start[1] + self.specification.height + self.specification.separation  ]
            basis_specification.invert = [ False , False , False , False ]
            return basis_specification
            
        if side == "top" :
            basis_specification.start = [ self.specification.start[0] + self.specification.length + self.specification.separation , 
                                         self.specification.start[1] ]
            basis_specification.invert = [ False , False , False , False ]
            return basis_specification
        
        if side == "bottom" :
            basis_specification.start = [ self.specification.start[0] + self.specification.length + self.specification.separation , 
                                         self.specification.start[1] + self.specification.height + self.specification.separation ]
            basis_specification.invert = [ True , True , False , False ]
            return basis_specification
            
        if side == "left" :
            this_specification = basis_specification.copy()
            this_specification.start = [ self.specification.start[0] + 2 * self.specification.length + 2 * self.specification.separation , 
                                         self.specification.start[1] ]
            this_specification.length = self.specification.height
            this_specification.height = self.specification.height
            this_specification.horizontal_number = self.specification.vertical_number
            this_specification.vertical_number = self.specification.vertical_number
            this_specification.invert = [ True , True , True , True ]
            return this_specification
            
        if side == "right" :
            this_specification = basis_specification.copy()
            this_specification.start = [ self.specification.start[0] + 2 * self.specification.length + 2 * self.specification.separation , 
                                         self.specification.start[1] + self.specification.height + self.specification.separation ]
            this_specification.length = self.specification.height
            this_specification.height = self.specification.height
            this_specification.horizontal_number = self.specification.vertical_number
            this_specification.vertical_number = self.specification.vertical_number
            this_specification.invert = [ True , True , True , True ]
            return this_specification



    def draw_basic( self ) :
        
        output = ""
        
        sides = []
        
        sides.append( 
                CrenellatedSide( 
                        self.get_side_specification( "front" )
                        )
                )
                
        sides.append( 
                CrenellatedSide( 
                        self.get_side_specification( "back" )
                        )
                )
        
        sides.append( 
                CrenellatedSide( 
                        self.get_side_specification( "top" )
                        )
                )
                
        sides.append( 
                CrenellatedSide( 
                        self.get_side_specification( "bottom" )
                        )
                )
                
        sides.append( 
                CrenellatedSide( 
                        self.get_side_specification( "left" )
                        )
                )
                
        sides.append( 
                CrenellatedSide( 
                        self.get_side_specification( "right" )
                        )
                )

        for side in sides :
            output += side.draw()

        return output
    
    def draw_extra( self ) :
        # Does nothing, here to be overridden
        return ""
    
    def draw( self ) :
        return self.draw_basic() + self.draw_extra()



#########################################################################

horizontal_number = 5
vertical_number = 3
depth = 2.0 # mm
total_length = 100.0 # mm
total_height = 40.0 # mm
separation = 7.0 # mm
stroke_width = 0.1 # str((1.0/3.543)*0.001) # mm, to be 0.001 px

start = [ 20.0 , 10.0 ]

columns = 3
rows = 4
column_offset = total_length*2 + total_height + separation*2.6
row_offset = total_height*2 + separation*2.0

out_string += init( 800 , 400 )

# Box sides
for i in range(columns) :
    for j in range(rows) :
        next_start = [ start[0] + i*column_offset , start[1] + j*row_offset ]
        specification = CrenellatedBoxSpecification(
                next_start ,
                total_length ,
                total_height ,
                depth ,
                horizontal_number ,
                vertical_number ,
                separation ,
                "" ,
                cut_colour ,
                cut_width
                )
        box = CrenellatedBox( specification )
        out_string += box.draw()



# Add cuts for molex pins
# Female first
for i in range(8) :
    molex_dimensions = [ 19.0 + i*0.5 , 4.0 + i*0.5 ] # mm
    x0 = start[0] + 1*(total_length*2 + separation*2 ) + total_height/2.0 - molex_dimensions[1]/2.0
    y0 = start[1] + depth + i*(total_height + separation) + total_height/2.0 - molex_dimensions[0]/2.0
    out_string += cut_rectangle( [ x0 , y0 ] , molex_dimensions[1] , molex_dimensions[0] )
#Male second
for i in range(8) :
    molex_dimensions = [ 21.0 + i*0.5 , 6.0 + i*0.5 ] # mm
    x0 = start[0] + column_offset + 1*(total_length*2 + separation*2 ) + total_height/2.0 - molex_dimensions[1]/2.0
    y0 = start[1] + depth + i*(total_height + separation) + total_height/2.0 - molex_dimensions[0]/2.0
    out_string += cut_rectangle( [ x0 , y0 ] , molex_dimensions[1] , molex_dimensions[0] )    
    

# LED mount test
led_width = 5.0 # mm
led_height = 5.0 # mm
layers = [ 1 , 5 , 10 , 20 , 30 , 40 , 50 , 60 , 70 , 80 , 90 , 100 ] 
k = 0
for i in range(4) :
    for j in range(3) :
        x0 = start[0] + depth*2 + led_width + 2*i*led_width
        y0 = start[1] + depth*2 + led_height + 2*j*led_height
        out_string += layer_engrave_rectangle( [ x0 , y0 ] , led_width , led_height , 100 , layers[k] )
        k += 1



# Arduino mount test
nano_length = 1.70 * 25.4
nano_width = 0.73 * 25.4
hole_radius = 0.07/2.0 * 25.4
inset = 0.06 * 25.4

x0 = start[0] + total_length/2.0 - nano_length/2.0 + inset
y0 = start[1] + 1*row_offset + depth + total_height/2.0 - nano_width/2.0 + inset

out_string += Circle( x0 , y0 , hole_radius , "#000000" , "none" , 0.001 ).draw()

x0 = start[0] + total_length/2.0 - nano_length/2.0 + inset
y0 = start[1] + 1*row_offset + depth + total_height/2.0 + nano_width/2.0 - inset

out_string += Circle( x0 , y0 , hole_radius , "#000000" , "none" , 0.001 ).draw()

x0 = start[0] + total_length/2.0 + nano_length/2.0 - inset
y0 = start[1] + 1*row_offset + depth + total_height/2.0 - nano_width/2.0 + inset

out_string += Circle( x0 , y0 , hole_radius , "#000000" , "none" , 0.001 ).draw()

x0 = start[0] + total_length/2.0 + nano_length/2.0 - inset
y0 = start[1] + 1*row_offset + depth + total_height/2.0 + nano_width/2.0 - inset

out_string += Circle( x0 , y0 , hole_radius , "#000000" , "none" , 0.001 ).draw()
                     
out_string += close()

with open( out_file , 'w' ) as out :
    out.write( out_string )


