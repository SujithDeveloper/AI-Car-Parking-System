import cv2
import pytesseract
import requests
import numpy as np
import sys

def num_plate(video_url):
    harcascade = "haarcascade_russian_plate_number.xml"
    nPlate = ""
    min_area = 500

    while True:

        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            bytes_array = bytes()
            for chunk in response.iter_content(chunk_size=1024):
                bytes_array += chunk
                a = bytes_array.find(b'\xff\xd8')
                b = bytes_array.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_array[a:b + 2]
                    bytes_array = bytes_array[b + 2:]
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    plate_cascade = cv2.CascadeClassifier(harcascade)
                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

                    for (x, y, w, h) in plates:
                        area = w * h

                        if area > min_area:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                        (255, 0, 255),
                                        2)

                            img_roi = img[y: y + h, x:x + w]
                            cv2.imshow("ROI", img_roi)
                            nPlate = pytesseract.image_to_string(img_roi).strip()
                    if len(nPlate.strip()) == 12:
                        break

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        else:
            print("Failed to retrieve the video stream.")
            break
        if nPlate:
            break
    cv2.destroyAllWindows()
    return nPlate
    sys.exit()