# AI-Car-Parking-System
This is my B.Tech last year project.


This paper introduce a car parking system with an application. 
In big cities many of us do not enjoy standing in long queues waiting for the parking space to be alloted. 
This project can be implemented in malls, metro stations, etc. To fasten the parking process.

This parking system have car identification and number plate recognition using machine learning and real time updation of available slots in application. 
Pre-booking is also available through the application. 

If any vehicle in front of the entry gate, using machine learning it will identify the vehicle. 
If it is a car, then identify the vehicle number and record the number and entry time and the gate will open if the parking space is available. 
The system will calculate the available slot through minimize the used space from total space.

We have an application and it will updated the information of available slots in real-time. 
We can create an account through the E-mail address or phone number and many of us have more than one vehicle so we can add the number of vehicles in one account. 
In the way out gate has an another camera and it will read the vehicle number and calculate the amount of payment. 
When we leave from the exit gate the system will generate a QR code for total payment amount. 
We can pay using that QR code provided in the parking place's display.

Here we have hardware and software sections and a database. In hardware section includes ESP32_Cam module, 16*2 LCD displays, Servo motors, IR Sensors and Computer. Software section includes Arduino IDE for upload code to ESP32_Cam module, Python for car and number plate detection (Here we detect car using YOLO and number plate using haarcascade trained file) and Android studio for making application. Here we use google firebase realtime database for store the sensor datas, parking slot datas and user signup datas.

The entry and exit gate have ESP32_Cam, LCD display, Servo motor and IR sensor. The camera will detect only for cars, so it will detect when a car come to the entry gate. Then it will detect the number plate and check the availability of the parking slots. If the slots are available, then the gate (servo motor) will open. An IR sensor placed back of the servo motor. When the car pass through the IR sensor, it will detect and close the gate. The LCD display will show the availability of space, number plate and all other informations. When a car entry, it will check the car is booked through the application or not. If not,the vehicle's number plate and entry time will store to the database.

The entry gate also detect the car and number plate and calculate the payment amount using entry time and exit time. The system will generate a QR code for the total payment amound and display it on the display. If the payment done, then the exit gate will open. When the car exit, the IR sensor will detect and the exit gate will close.
