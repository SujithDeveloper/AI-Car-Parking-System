const int irPin = 2;  // GPIO pin connected to the OUT pin of the IR sensor

void setup() {
  pinMode(irPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  int sensorValue = digitalRead(irPin);
  if (sensorValue == LOW) {
    Serial.println("Object detected!");
  } else {
    Serial.println("No object detected.");
  }
  delay(1000);
}
