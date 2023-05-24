#include "WifiCam.hpp"
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <ESP32Servo.h>
//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

static const char* WIFI_SSID = "Dex22";
static const char* WIFI_PASS = "AFTR22bE";
// Insert Firebase project API Key
#define API_KEY "AIzaSyCqzBJ3gArWr2AZWE3VSo58NXrqVa5VDqY"
// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://ai-car-parking-system-default-rtdb.firebaseio.com/" 

esp32cam::Resolution initialResolution;

WebServer server(80);

//Define Firebase Data object
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
bool signupOK = false;

const int irPin = 12;
const int servoPin = 2;  // GPIO pin connected to the signal wire of the servo motor
Servo myservo;

String servo1;
int irValue;
String servoff = "OFF";

void
setup()
{

  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 1);

  pinMode(irPin, INPUT);
  Serial.begin(115200);
  Serial.println();
  delay(2000);

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi failure");
    delay(5000);
    ESP.restart();
  }
  Serial.println("WiFi connected");

  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("camera initialize failure");
      delay(5000);
      ESP.restart();
    }
    Serial.println("camera initialize success");
  }

  Serial.println("camera starting");
  Serial.print("http://");
  Serial.println(WiFi.localIP());

  addRequestHandlers();
  server.begin();

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

  myservo.attach(servoPin, 500, 2400);  // Set the servo pin and the pulse width range (microseconds)
  myservo.write(90);  // Set the initial position of the servo motor
  delay(2000);
  
}

void
loop()
{
  server.handleClient();
  
  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();
    server.handleClient();

    Firebase.RTDB.getString(&fbdo, "/Sensor_Status/Servo1");
    servo1 = fbdo.stringData();
    server.handleClient();
    if (servo1 == "ON"){
      // Rotate servo motor in forward direction (0 to 90 degrees)
      for (int pos = 0; pos <= 90; pos++) {
        myservo.write(pos);   // Set servo position
        server.handleClient();
      }
      server.handleClient();
      irValue = digitalRead(irPin);
      while (irValue == HIGH) {
        server.handleClient();
        irValue = digitalRead(irPin);
      }
      Firebase.RTDB.setString(&fbdo, "Sensor_Status/Servo1", servoff);
      server.handleClient();
      // Rotate servo motor in reverse direction (90 to 0 degrees)
      for (int pos = 90; pos >= 0; pos--) {
        myservo.write(pos);   // Set servo position
        server.handleClient();
      }

    }

  }  
  
}
