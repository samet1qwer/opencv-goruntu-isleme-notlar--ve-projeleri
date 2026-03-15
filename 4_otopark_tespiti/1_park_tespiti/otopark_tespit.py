import cv2
import numpy as np
import pickle

width = 27
height = 15

video = cv2.VideoCapture("video.mp4")

with open("../0_kordinat_tespiti/cordinates", "rb") as f:
    cordinates = pickle.load(f)

def check_park(img, original):
    space_counter = 0
    for pos in cordinates:
        crop_img = img[pos[1]:pos[1] + height, pos[0]:pos[0] + width]
        count = cv2.countNonZero(crop_img)

        if count < 150:
            color = (0, 255, 0)
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(original, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cv2.putText(original, str(count), (pos[0], pos[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    return space_counter


while True:
    ret, frame = video.read()

    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)  
        continue

    img_gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur   = cv2.GaussianBlur(img_gray, (7, 7), 0)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_thresh, 5)
    kernel     = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    free_spaces = check_park(img_dilate, frame)
    total_spaces = len(cordinates)
    cv2.rectangle(frame, (0, 0), (220, 50), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, f"Bos: {free_spaces} / {total_spaces}",
                (1, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.1,
                (0, 255, 0) if free_spaces > 0 else (0, 0, 255), 2)

    cv2.imshow("Otopark", frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()