import cv2
from time import sleep
import requests
import io
import json
import os
import random

def perform_ocr(img_path):
    print("Picture is Detected")

    img = cv2.imread(img_path)

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
                           files={img_path: file_bytes},
                           data={"apikey": "helloworld", "language": "eng"})

    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    print("Detected Text:\n", text_detected)

    print("Writing to file...")
    with open("text_detected.txt", "a+", encoding="utf-8") as f:
        f.write(text_detected + "\n")
    print("✅ Text saved successfully!")

    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# -----------------------------------------
# 🔥 Entry Point
# -----------------------------------------

print("Choose input mode:")
print("1 - Use Webcam")
print("2 - Use Image Path")

mode = input("Enter your choice (1 or 2): ")

if mode == '1':
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    sleep(2)

    print("Press 'S' to capture, 'Q' to quit...")

    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                filename = 'images.jpg'
                cv2.imwrite(filename=filename, img=frame)
                r = random.randint(1, 20000000)
                img_file = 'images' + str(r) + '.jpg'
                cv2.imwrite('data/' + img_file, frame)
                webcam.release()
                cv2.destroyAllWindows()
                perform_ocr(filename)
                os.remove(filename)
                break
            elif key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break
        except KeyboardInterrupt:
            webcam.release()
            cv2.destroyAllWindows()
            break

elif mode == '2':
    img_path = input("Enter the full path of your image: ").strip()
    if os.path.exists(img_path):
        perform_ocr(img_path)
    else:
        print("❌ Invalid path. File does not exist.")
else:
    print("❌ Invalid choice. Please enter 1 or 2.")
