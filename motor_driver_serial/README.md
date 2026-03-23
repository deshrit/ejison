# Motor Driver Serial

This library communicates with Arduino Uno board to run two `28BYJ-48` 5V stepper 
motors with `ULN2003` drivers.

# Serial Commands

The baud rate of Arduino Uno board is set to be `115200`.

Commands to control the motors are:

For testing:

- `s`: Stop both motors

- `m s1 s2`: Run left and right motor with `s1` and `s2` speed respectively (range `±300`)

- `c`: Continue last speed

- `p`: Print current speed

- `t`: Print motor steps in same order as speed separated by a space

- `r`: Reset motor steps

Running with ROS:

- `d s1 s2`: Same as `m` and also publish motor steps along side

