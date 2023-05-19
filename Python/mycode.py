import cv2
import requests
import numpy as np
import pytesseract

from cars_Detection import car_detect
from nplate_Detection import num_plate

video_url1 = "http://192.168.18.145/800x600.mjpeg"
video_url2 = "http://192.168.18.147/800x600.mjpeg"

IR1 = True
IR2 = True

while True:
    if IR1 == True:
        car = car_detect(video_url1)
        print("Car Detected")
        plate = num_plate(video_url1)
        print(plate)

    if IR2 == True:
        car = car_detect(video_url2)
        print("Car Detected")
        plate = num_plate(video_url2)
        print(plate)


print("Good")