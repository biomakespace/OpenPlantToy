#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

file_name = "test_rejig_2.svg"

thicken = 0

PROPERTY_REGEX = "stroke-width=\\\"\d*(\\.\d*)?\\\""
STYLE_REGEX = "stroke-width:\d*(\\.\d*)?"

property_replace = "stroke-width=\"{N}\""
style_replace = "stroke-width:{N}"
NUMBER_REPLACE = "{N}"

thick_width = "1.0"
thin_width = "0.001"

# Get full svg file
with open( file_name , 'r' ) as file :
    file_contents = file.read()



if thicken :
    # Set up the numbers in the replacement strings
    property_replace = property_replace.replace( NUMBER_REPLACE , thick_width )
    style_replace = style_replace.replace( NUMBER_REPLACE , thick_width )
    # Set the stroke widths in the SVG
    file_contents = re.sub( PROPERTY_REGEX , property_replace , file_contents )
    file_contents = re.sub( STYLE_REGEX , style_replace , file_contents )
else :
    # Set up the numbers in the replacement strings
    property_replace = property_replace.replace( NUMBER_REPLACE , thin_width )
    style_replace = style_replace.replace( NUMBER_REPLACE , thin_width )
    # Set the stroke widths in the SVG
    file_contents = re.sub( PROPERTY_REGEX , property_replace , file_contents )
    file_contents = re.sub( STYLE_REGEX , style_replace , file_contents )
    


with open( file_name , 'w' ) as file :
    file.write( file_contents )