#include <Servo.h>

Servo myservo;  // Create a servo object

void setup() {
  myservo.attach(9);  // Attaching the servo to pin 9
}

void loop() {
  // Rotate servo motor in forward direction (0 to 180 degrees)
  for (int pos = 0; pos <= 180; pos++) {
    myservo.write(pos);   // Set servo position
    delay(15);            // Delay for servo to reach position
  }

  delay(1000);  // Delay for 1 second

  // Rotate servo motor in reverse direction (180 to 0 degrees)
  for (int pos = 180; pos >= 0; pos--) {
    myservo.write(pos);   // Set servo position
    delay(15);            // Delay for servo to reach position
  }

  delay(1000);  // Delay for 1 second
}

