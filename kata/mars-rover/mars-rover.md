# Mars Rover Kata

## Your Task

You’re part of the team that explores Mars by sending remotely controlled vehicles to the surface of the planet. Develop an API that translates the commands sent from earth to instructions that are understood by the rover.

## Requirements

* You are given the initial starting point (x,y) of a rover and the direction (N,S,E,W) it is facing.
* The rover receives a character array of commands.
* Implement commands that move the rover forward/backward (F,B).
* Implement commands that turn the rover left/right (L,R).
* Implement wrapping at edges. Planets are spheres after all.

## Example

Here is an example:
– Let’s say that the rover is located at 0,0 facing North on a 100×100 grid.
– Given the command “FFRFF” would put the rover at 2,2 facing East.