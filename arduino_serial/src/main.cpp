#include <Arduino.h>
#include <AccelStepper.h>

const uint8_t M1_PIN1 = 8, M1_PIN2 = 9, M1_PIN3 = 10, M1_PIN4 = 11; // Motor 1
const uint8_t M2_PIN1 = 4, M2_PIN2 = 5, M2_PIN3 = 6, M2_PIN4 = 7; // Motor 2

const uint8_t STEPS_PER_REVOLUTION = 64; // 28BYJ motor's steps
const float DEGREE_PER_REVOLUTION = 5.625; // After 64 steps of motor axial moves 5.625 degrees due to gear reduction

float deg_to_steps(float deg) {
  return (STEPS_PER_REVOLUTION / DEGREE_PER_REVOLUTION) * deg;
}

AccelStepper motor_right(AccelStepper::FULL4WIRE, M1_PIN1, M1_PIN3, M1_PIN2, M1_PIN4);
AccelStepper motor_left(AccelStepper::FULL4WIRE, M2_PIN1, M2_PIN3, M2_PIN2, M2_PIN4);

/* Command from serial
* s - stop all
* l - move left only
* r - move right only
* b - move both
*/
char command = 's';

void setup() {
  Serial.begin(9600);
  while(!Serial);

  motor_left.setMaxSpeed(1000);
  motor_left.setSpeed(200);

  motor_right.setMaxSpeed(1000);
  motor_right.setSpeed(-200);
}

void loop() {

  if(Serial.available() > 0) {
    command = Serial.read();
  }

  switch(command) {
    case 'l':
    motor_left.runSpeed();
    motor_right.stop();
    break;

    case 'r':
    motor_right.runSpeed();
    motor_left.stop();
    break;

    case 'b':
    motor_left.runSpeed();
    motor_right.runSpeed();
    break;

    case 's':
    default:
    motor_left.stop();
    motor_right.stop();
    break;
  }

}
