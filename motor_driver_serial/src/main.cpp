#include <Arduino.h>
#include <AccelStepper.h>

# define BUFFER_SIZE 16

const uint8_t M1_PIN1 = 4, M1_PIN2 = 5, M1_PIN3 = 6, M1_PIN4 = 7; // Left motor
const uint8_t M2_PIN1 = 8, M2_PIN2 = 9, M2_PIN3 = 10, M2_PIN4 = 11; // Right motor

const uint8_t STEPS_PER_REVOLUTION = 64; // 28BYJ motor's steps
const float DEGREE_PER_REVOLUTION = 5.625; // After 64 steps of motor axial moves 5.625 degrees due to gear reduction

float deg_to_steps(float deg) {
  return (STEPS_PER_REVOLUTION / DEGREE_PER_REVOLUTION) * deg;
}

AccelStepper motor_left(AccelStepper::FULL4WIRE, M1_PIN1, M1_PIN3, M1_PIN2, M1_PIN4);
AccelStepper motor_right(AccelStepper::FULL4WIRE, M2_PIN1, M2_PIN3, M2_PIN2, M2_PIN4);

int speed_left = 150, speed_right = 150;
bool move = false;

const int PUBLISH_INTERVAL_MS = 100;
unsigned long last_publish = 0;
bool publish = false;

long last_left_steps = 0, last_right_steps = 0;

/*
* Serial Commands
*
* s: Stop both motors
*
* For testing:
*
* m s1 s2: Run left and right motor with `s1` and `s2` speed respectively (speed range `±300`)
* c: Continue last speed
* p: Print current speed
* t: Print motor steps in same order as speed
* r: Reset motor steps
*
*
* Running with ROS:
*
* d s1 s2: Same as m and publish motor steps in same order as speed
* 
*/
char command[BUFFER_SIZE];
uint8_t buffer_index = 0;

void setup() {
  Serial.begin(115200);
  while(!Serial);

  motor_left.setMaxSpeed(300);
  motor_left.setSpeed(-speed_left);

  motor_right.setMaxSpeed(1000);
  motor_right.setSpeed(speed_right);
}

void process_command(char *command) {
  switch (command[0]) {
    case 's':
      move = false;
      publish = false;
      break;

    case 'c':
      motor_left.setSpeed(-speed_left);
      motor_right.setSpeed(speed_right);
      move = true;
      break;

    case 'm':
      if(sscanf(command+1, "%d %d", &speed_left, &speed_right) == 2) {
        if(speed_left > 300) speed_left = 300;
        if(speed_left < -300) speed_left = -300;
        motor_left.setSpeed(-speed_left);

        if(speed_right > 300) speed_right = 300;
        if(speed_right < -300) speed_right = -300;
        motor_right.setSpeed(speed_right);
        move = true;
      }
      break;

    case 'd':
      publish = true;
      if(sscanf(command+1, "%d %d", &speed_left, &speed_right) == 2) {
        if(speed_left > 300) speed_left = 300;
        if(speed_left < -300) speed_left = -300;
        motor_left.setSpeed(-speed_left);

        if(speed_right > 300) speed_right = 300;
        if(speed_right < -300) speed_right = -300;
        motor_right.setSpeed(speed_right);
        move = true;
      }
      break;

    case 'p':
      Serial.print(speed_left);
      Serial.print(" ");
      Serial.println(speed_left);
      break;
    
    case 't':
      Serial.print(last_left_steps);
      Serial.print(" ");
      Serial.println(last_right_steps);
      break;

    case 'r':
      move = false;
      motor_left.setCurrentPosition(0);
      motor_right.setCurrentPosition(0);
      break;

    default:
      break;
  }
}

void read_serial() {
  while(Serial.available()) {
    char c = Serial.read();
    if(c == '\n') {
      command[buffer_index] = '\0';
      process_command(command);
      buffer_index = 0;
    } else {
      if(buffer_index < BUFFER_SIZE-1) {
        command[buffer_index++] = c;
      }
    }
  }
}

void move_motors() {
  if(!move) {
    motor_left.stop();
    motor_right.stop();
    return;
  }
  motor_left.runSpeed();
  motor_right.runSpeed();
}

void update_steps()
{
  long current_left_steps = motor_left.currentPosition();
  long current_right_steps = motor_right.currentPosition();

  if(current_left_steps != last_left_steps || current_right_steps != last_right_steps)
  {
    last_left_steps = current_left_steps;
    last_right_steps = current_right_steps;
  }
}

void publish_steps() {
  if(!publish) return;
  unsigned long now = millis();
  if(now - last_publish >= PUBLISH_INTERVAL_MS) {
    last_publish = now;
    Serial.print(last_left_steps);
    Serial.print(" ");
    Serial.println(last_right_steps);
  }
}


void loop() {
  read_serial();
  move_motors();
  update_steps();
  publish_steps();
}


////////////////////////////////////////////////////////////////////////////////////

// #include <Arduino.h>

// #define BUFFER_SIZE 32

// char command[BUFFER_SIZE] = "default";
// uint8_t buffer_index = 0;

// void read_serial() {
//   while(Serial.available()) {
//     char c = Serial.read();
//     if(c == '\n') {
//       command[buffer_index] = '\0';
//       buffer_index = 0;
//     } else {
//       if(buffer_index < BUFFER_SIZE-1) {
//         command[buffer_index++] = c;
//       }
//     }
//   }
// }


// void setup() {
//   Serial.begin(115200);
// }

// void loop() {
//   read_serial();
//   Serial.println(command);
//   delay(100);
// }