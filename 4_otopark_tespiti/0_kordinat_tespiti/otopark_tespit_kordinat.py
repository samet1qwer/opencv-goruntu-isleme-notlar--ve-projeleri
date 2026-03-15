import cv2
import pickle

width = 27
height = 15



try:
    with open("cordinates", "rb") as f:
        cordinates = pickle.load(f)
except:
    cordinates = []


def mause_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        cordinates.append((x, y))
        print(cordinates)
    if event == cv2.EVENT_RBUTTONDOWN:
        cordinates.pop()
        print(cordinates)
    with open("cordinates", "wb") as f:
        pickle.dump(cordinates, f)









while True:
    img = cv2.imread("otopark.png")
    
    
    cv2.namedWindow("Otopark Tespiti")
    cv2.setMouseCallback("Otopark Tespiti", mause_click)
    for cord in cordinates:
        cv2.rectangle(img, cord, (cord[0] + width, cord[1] + height), (0, 0, 255), 2)
    cv2.imshow("Otopark Tespiti", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    cv2.waitKey(1)
    
cv2.destroyAllWindows()




