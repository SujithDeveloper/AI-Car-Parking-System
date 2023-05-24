// Include WiFi library
#include <Arduino.h>
#if defined(ESP32) || defined(PICO_RP2040)
#include <WiFi.h>
#elif defined(ESP8266)
#include <ESP8266WiFi.h>
#endif
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
#include <Firebase_ESP_Client.h>
#include <Servo.h>
Servo myservo1;  // Create a servo object
Servo myservo2;
//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
#define WIFI_SSID "Dex22"
#define WIFI_PASSWORD "AFTR22bE"

// Insert Firebase project API Key
#define API_KEY "AIzaSyCqzBJ3gArWr2AZWE3VSo58NXrqVa5VDqY"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://ai-car-parking-system-default-rtdb.firebaseio.com/" 

//Define Firebase Data object
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
String servo1 = "OFF";
String stringValue;
bool signupOK = false;

const int servo1Pin = D3;
const int servo2Pin = D4;
const int ir1Pin = D5; 
const int ir2Pin = D6;

int ir1Value;
int ir2Value;

void setup(){

  pinMode(ir1Pin, INPUT);
  pinMode(ir2Pin, INPUT);

  myservo1.attach(servo1Pin);  // Attach the servo to the specified pin
  myservo2.attach(servo2Pin);
  myservo1.write(0);
  myservo2.write(0);

  lcd.begin(16, 2);
  lcd.init();
  lcd.backlight();
  
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  
  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

}

void loop(){
  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();
    // Write an Int number on the database path test/int
    Firebase.RTDB.setString(&fbdo, "Sensor/Data", servo1);
    delay(10000);
    Firebase.RTDB.getString(&fbdo, "/Sensor_Status/Servo2");
    stringValue = fbdo.stringData();
    if (stringValue == "OFF"){
      servo1 = "ON";
      Firebase.RTDB.setString(&fbdo, "Sensor/Data", servo1);
      lcd.setCursor(0, 0);
      lcd.print(" Welcome: ");
      delay(500);
      lcd.setCursor(0, 1);
      lcd.print(" GuyZzz... ");
      delay(2000);
      lcd.clear();
      delay(500);
      servo1 = "OFF";

      // Rotate servo motor in forward direction (0 to 90 degrees)
      for (int pos = 0; pos <= 90; pos++) {
        myservo1.write(pos);   // Set servo position
        delay(15);            // Delay for servo to reach position
      }

      ir1Value = digitalRead(ir1Pin);
      while (ir1Value == HIGH) {
        delay(100);
        ir1Value = digitalRead(ir1Pin);
      }
      
      // Rotate servo motor in reverse direction (90 to 0 degrees)
      for (int pos = 90; pos >= 0; pos--) {
        myservo1.write(pos);   // Set servo position
        delay(15);            // Delay for servo to reach position
      }

      delay(1000);

      // Rotate servo motor in forward direction (0 to 90 degrees)
      for (int pos = 0; pos <= 90; pos++) {
        myservo2.write(pos);   // Set servo position
        delay(15);            // Delay for servo to reach position
      }

      ir2Value = digitalRead(ir2Pin);
      while (ir2Value == HIGH) {
        delay(100);
        ir2Value = digitalRead(ir2Pin);
      }

      // Rotate servo motor in reverse direction (90 to 0 degrees)
      for (int pos = 90; pos >= 0; pos--) {
        myservo2.write(pos);   // Set servo position
        delay(15);            // Delay for servo to reach position
      }

      delay(1000);

      
     }
    
   }
}
