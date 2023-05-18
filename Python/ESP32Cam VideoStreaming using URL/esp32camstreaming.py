import cv2
import requests
import numpy as np

video_url = "http://192.168.18.145/800x600.mjpeg"

while True:
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        bytes_array = bytes()
        for chunk in response.iter_content(chunk_size=1024):
            bytes_array += chunk
            a = bytes_array.find(b'\xff\xd8')
            b = bytes_array.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes_array[a:b+2]
                bytes_array = bytes_array[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow("ESP32-CAM Video", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    else:
        print("Failed to retrieve the video stream.")
        break

cv2.destroyAllWindows()
