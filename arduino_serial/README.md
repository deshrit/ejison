# Arduino Serial

This library communicates with Arduino Uno board to run the two 28BYJ48 5V stepper 
motors in fixed default speed.

# Serial Commands

The fixed baud rate of Arduino Uno board is `9600`.

Commands to control the motors with single character are:

```text
s - stop both motors
l - run only left motor
r - run only right motor
b - run both motor
```
