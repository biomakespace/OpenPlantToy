
# Open Plant Toy

A project to build an educational toy to illustrate how genetic circuits are constructed and how components of genetic circuits interact. The toy will take the form of a series of blocks, each representing a part of the genetic puzzle, which are connected together via some universal connection. Certain blocks will react in certain ways, for example by turning on an LED or making a sound, when the constructed circuit meets the required conditions for those things to happen. These outputs are intended to be tangible representations of real outputs from genetic circuits, such as synthesised proteins.

The project is being undertaken by members of the [Biomakespace](https://biomake.space/home) in Cambridge, UK.

# Wiki

A fairly good Wiki is being constructed on the repository, so instead of repeating content below you will find a brief summary of the areas of the repository and links to the Wiki pages that explain them in a bit more detail.

# Orientation

All links below are to the master branch which _should_ be actually mostly working, but in case you want the most up to date code you can check out develop instead.

## [control](https://github.com/biomakespace/OpenPlantToy/tree/master/control)

Here you'll find the program that control the circuit as a whole. Its role is to understand which pieces of the circuit are connected to which other pieces & in what order based on the data collected by the base unit, and instruct the reactive parts of the circuit to take the appropriate actions.

The control code is well explained on [its Wiki page](https://github.com/biomakespace/OpenPlantToy/wiki/Controller-Code).

## [components](https://github.com/biomakespace/OpenPlantToy/tree/master/components)

Here you'll find a series of folders which have the Arduino code snippets. These should be ready to upload directly to Arduinos (designed for Nanos, but should be compatible with various versions). Wire up the LED/serial connections as indicated in the control section, connect the base unit to the computer then, run the control script and join the fun! Note that each component that we've designed so far has to have its own folder because {Arduino IDE things}. The full detail of what is going on in the component code is explained [relevant Wiki page](https://github.com/biomakespace/OpenPlantToy/wiki/Component-Code).

By the way, don't edit those by hand! Or do, it's open source after all and you can do what you want, but it's not recommended. Imagine a complex genetic circuit with tens of components, and imagine you discover a bug in the code for all the components (or introduce an improvement/feature). Are you going to update all the files manually?

If you answered yes to this, read up on [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) and check out the included Python script for automatically generating code for each individual circuit component, which is explained in some detail on [its Wiki page](https://github.com/biomakespace/OpenPlantToy/wiki/Component-Code-Generator-Script). In line with this, to keep the script from being somewhat messy and since the most of the code is common across all the components we designed so far, there are two .ino snippet files in this folder which are used as templates for generating the individual component code files.

## [connection diagrams](https://github.com/biomakespace/OpenPlantToy/tree/master/connection_diagrams)

This is fairly self-explanatory. If you want to dive right into playing with the toy, get the code loaded onto the Arduinos, connect them as instructed on [the Wiki page](https://github.com/biomakespace/OpenPlantToy/wiki/Component-Connections), connect one to a computer via USB, run the Python script there, and you're away. Enjoy! 
