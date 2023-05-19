import cv2
import numpy as np
import requests
import sys

def car_detect(video_url):
    net = cv2.dnn.readNet('yolov3_training_last.weights', 'yolov3_testing.cfg')

    classes = []
    with open("classes.txt", "r") as f:
        classes = f.read().splitlines()

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(100, 3))
    detect = False

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

                    height, width, _ = img.shape
                    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
                    net.setInput(blob)
                    output_layers_names = net.getUnconnectedOutLayersNames()
                    layerOutputs = net.forward(output_layers_names)

                    boxes = []
                    confidences = []
                    class_ids = []

                    for output in layerOutputs:
                        for detection in output:
                            scores = detection[5:]
                            class_id = np.argmax(scores)
                            confidence = scores[class_id]
                            if confidence > 0.2:
                                center_x = int(detection[0] * width)
                                center_y = int(detection[1] * height)
                                w = int(detection[2] * width)
                                h = int(detection[3] * height)

                                x = int(center_x - w / 2)
                                y = int(center_y - h / 2)

                                boxes.append([x, y, w, h])
                                confidences.append((float(confidence)))
                                class_ids.append(class_id)

                    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

                    if len(indexes) > 0:
                        for i in indexes.flatten():
                            x, y, w, h = boxes[i]
                            label = str(classes[class_ids[i]])
                            confidence = str(round(confidences[i], 2))
                            color = colors[i]
                            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                            cv2.putText(img, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)

                    cv2.imshow('Image', img)
                    print(class_ids)
                    key = cv2.waitKey(1)
                    if 2 in class_ids:
                        detect = True
                        break

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        else:
            print("Failed to retrieve the video stream.")
            break
        if detect == True:
            break

    cv2.destroyAllWindows()
    return detect
    sys.exit()