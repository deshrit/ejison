# Arduino Serial

This library communicates with Arduino Uno board to run two `28BYJ48` 5V stepper motors with `ULN2003` drivers.

# Serial Commands

The baud rate of Arduino Uno board is set to be `115200`.

Commands to control the motors are:

- `s`: Stop both motors

- `m s1 s2`: Run left and right motor with `s1` and `s2` speed respectively (range `±300`)

- `c`: Continue last speed

- `p`: Print current speed

