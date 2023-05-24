#include <ESP32Servo.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

const int servoPin = 2;  // GPIO pin connected to the signal wire of the servo motor
Servo myservo;

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 1);
  myservo.attach(servoPin, 500, 2400);  // Set the servo pin and the pulse width range (microseconds)
  myservo.write(90);  // Set the initial position of the servo motor
  delay(2000);
}

void loop() {
  // Rotate servo motor in forward direction (0 to 90 degrees)
  for (int pos = 0; pos <= 90; pos++) {
    myservo.write(pos);   // Set servo position
    delay(15);            // Delay for servo to reach position
  }

  delay(1000);  // Delay for 1 second

  // Rotate servo motor in reverse direction (90 to 0 degrees)
  for (int pos = 90; pos >= 0; pos--) {
    myservo.write(pos);   // Set servo position
    delay(15);            // Delay for servo to reach position
  }

  delay(1000);  // Delay for 1 second
}
