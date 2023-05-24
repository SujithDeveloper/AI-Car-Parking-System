import cv2
import tkinter as tk
from PIL import Image, ImageTk
import datetime
import time
from cars_Detection import car_detect
from nplate_Detection import num_plate

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ai-car-parking-system-firebase-adminsdk-4czki-3102d6d135.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://ai-car-parking-system-default-rtdb.firebaseio.com/'})

video_url1 = "http://192.168.18.147/800x600.mjpeg"
video_url2 = "http://192.168.18.145/800x600.mjpeg"

Number_of_Parking_Slots = 3
Pay_Amount_per_Minute = 1
available_slots = Number_of_Parking_Slots
pay_per_minute = Pay_Amount_per_Minute

ref = db.reference('/')
sensor_status = ref.child('Sensor_Status')
sensor_status.set(dict(Servo1='OFF', Servo2='OFF', LCD1='3 Slots Available', LCD2='Exit'))
slot_status = ref.child('Slot_Status')
slot_status.set({'Available_Slots': '3'})


def pay(time1_str, time2_str):

    # Split the string at the colon and convert hours and minutes to float
    hours1, minutes1 = map(float, time1_str.split(":"))
    hours2, minutes2 = map(float, time2_str.split(":"))

    h1_minutes = hours1 * 60
    h2_minutes = hours2 * 60

    # Combine hours and minutes as a float value
    time1_minute = h1_minutes + minutes1
    time2_minute = h2_minutes + minutes2

    time_difference = time1_minute - time2_minute
    return time_difference

def payment_window(entry_time, exit_time, payment_amount):
    cv2.destroyAllWindows()

    def confirmation_page():
        def button_click():
            window.destroy()

        # Hide the current page
        current_page.grid_forget()

        # Create and display the new page
        new_page = tk.Frame(window)
        new_page.grid()

        # Load and display the image
        image_path = "Payment_Success.jpg"
        image = Image.open(image_path)
        new_size = (500, 500)  # Adjust the image size (width, height)
        resized_image = image.resize(new_size)
        photo = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(new_page, image=photo)
        image_label.grid(row=0, column=0, columnspan=2)

        # Add widgets to the new page
        label = tk.Label(new_page, text="Payment Successfully!", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=2)

        # Create and display the button
        button = tk.Button(new_page, text="Exit", command=button_click, bg="blue")
        button.grid(row=4, column=0, columnspan=2)


    # Create the main window
    window = tk.Tk()

    # Set the window title
    window.title("Payment Window")

    # Create the initial page
    current_page = tk.Frame(window)
    current_page.grid()



    # Load and display the image
    image_path = "QR_Code.jpg"
    image = Image.open(image_path)
    new_size = (500, 500)  # Adjust the image size (width, height)
    resized_image = image.resize(new_size)
    photo = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(current_page, image=photo)
    image_label.grid(row=0, column=0, columnspan=2)

    # Display the text
    text_label = tk.Label(current_page, text="Entry Time : " + entry_time, font=("Arial", 14))
    text_label.grid(row=1, column=0, columnspan=2)

    text_label = tk.Label(current_page, text="Exit Time   : " + exit_time, font=("Arial", 14))
    text_label.grid(row=2, column=0, columnspan=2)

    text_label = tk.Label(current_page, text="Pay Amount : " + str(payment_amount) + " Rs.", font=("Arial", 18))
    text_label.grid(row=3, column=0, columnspan=2)

    # Create and display the button
    button = tk.Button(current_page, text="Pay Now", command=confirmation_page, bg="blue")
    button.grid(row=4, column=0, columnspan=2)

    # Configure the grid weights
    current_page.grid_rowconfigure(0, weight=1)
    current_page.grid_columnconfigure(0, weight=1)

    # Start the main event loop
    window.mainloop()


while True:
    if available_slots != 0:
        entry_car = car_detect(video_url1)
        if entry_car == True:
            print(" Entry Car Detected")
            db.reference('/Sensor_Status').update({'LCD1': 'Car Detected'})
            entry_plate = num_plate(video_url1)
            print(entry_plate)
            db.reference('/Sensor_Status').update({'LCD1': entry_plate})
            entry_time = datetime.datetime.now().strftime("%H:%M")
            slot_data = db.reference('/Slot_Status').get()
            if entry_plate in str(slot_data):
                if db.reference('/Slot_Status/' + entry_plate + '/Booked').get() == 'Yes':
                    db.reference('/Slot_Status/' + entry_plate).update({'Entry': 'Yes'})
                    db.reference('/Sensor_Status').update({'LCD1': 'Go for Park'})
                    db.reference('/Sensor_Status').update({'Servo1': 'ON'})
                    while db.reference('/Sensor_Status/Servo1').get() == 'ON':
                        time.sleep(0.05)
                    available_slots = available_slots - 1
                    db.reference('/Slot_Status').update({'Available_Slots': available_slots})
                    db.reference('/Sensor_Status').update({'LCD1': str(available_slots) + ' Slots Available'})
                else:
                    db.reference('/Sensor_Status').update({'LCD1': 'Already Entry'})
            else:
                slot_status.update({entry_plate: {'Entry_Time': entry_time, 'Booked': 'NO'}})
                db.reference('/Sensor_Status').update({'LCD1': 'Go for Park'})
                db.reference('/Sensor_Status').update({'Servo1': 'ON'})
                while db.reference('/Sensor_Status/Servo1').get() == 'ON':
                    time.sleep(0.05)
                available_slots = available_slots - 1
                db.reference('/Slot_Status').update({'Available_Slots': available_slots})
                db.reference('/Sensor_Status').update({'LCD1': str(available_slots) + ' Slots Available'})

    exit_car = car_detect(video_url2)
    if exit_car == True:
        print("Exit Car Detected")
        db.reference('/Sensor_Status').update({'LCD2': 'Car Detected'})
        exit_plate = num_plate(video_url2)
        print(exit_plate)
        slot_data = db.reference('/Slot_Status').get()
        while exit_plate not in str(slot_data):
            print('Fake Number plate Detected')
            db.reference('/Sensor_Status').update({'LCD2': 'Fake Number plate Detected'})
            exit_plate = num_plate(video_url2)
            print(exit_plate)
            slot_data = db.reference('/Slot_Status').get()
        db.reference('/Sensor_Status').update({'LCD2': exit_plate})
        exit_time = datetime.datetime.now().strftime("%H:%M")
        if db.reference('/Slot_Status/' + exit_plate + '/Booked').get() == 'Yes':
            booked_exit_time = db.reference('/Slot_Status/' + exit_plate + '/Exit_Time').get()
            pay_time = pay(exit_time, booked_exit_time)
            pay_amount = pay_time * pay_per_minute
            if pay_amount <= 0:
                db.reference('/Slot_Status/' + exit_plate).update({'Entry': 'No'})
                db.reference('/Sensor_Status').update({'LCD2': 'Thank You! Come Again'})
                db.reference('/Sensor_Status').update({'Servo2': 'ON'})
                while db.reference('/Sensor_Status/Servo2').get() == 'ON':
                    time.sleep(0.05)
                db.reference('/Sensor_Status').update({'LCD2': 'Exit'})
            else:
                db.reference('/Sensor_Status').update({'LCD2': 'Pay for Exit'})
                payment_window(booked_exit_time, exit_time, pay_amount)
                db.reference('/Sensor_Status').update({'LCD2': 'Thank You! Come Again'})
                db.reference('/Sensor_Status').update({'Servo2': 'ON'})
                while db.reference('/Sensor_Status/Servo2').get() == 'ON':
                    time.sleep(0.05)
                available_slots = available_slots + 1
                db.reference('/Slot_Status').update({'Available_Slots': available_slots})
                db.reference('/Sensor_Status').update({'LCD1': str(available_slots) + ' Slots Available'})
                db.reference('/Sensor_Status').update({'LCD2': 'Exit'})
                db.reference('/Slot_Status/' + exit_plate).delete()
        else:
            slot_entry_time = db.reference('/Slot_Status/' + exit_plate + '/Entry_Time').get()
            pay_time = pay(exit_time, slot_entry_time)
            pay_amount = pay_time * pay_per_minute
            db.reference('/Sensor_Status').update({'LCD2': 'Pay for Exit'})
            payment_window(slot_entry_time, exit_time, pay_amount)
            db.reference('/Sensor_Status').update({'LCD2': 'Thank You! Come Again'})
            db.reference('/Sensor_Status').update({'Servo2': 'ON'})
            while db.reference('/Sensor_Status/Servo2').get() == 'ON':
                time.sleep(0.05)
            available_slots = available_slots + 1
            db.reference('/Slot_Status').update({'Available_Slots': available_slots})
            db.reference('/Sensor_Status').update({'LCD1': str(available_slots) + ' Slots Available'})
            db.reference('/Sensor_Status').update({'LCD2': 'Exit'})
            db.reference('/Slot_Status/' + exit_plate).delete()


print("Good")

