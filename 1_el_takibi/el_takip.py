import cv2
import mediapipe as mp

width = 400
height = 400

vide_cam = cv2.VideoCapture(0)

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()

mp_draw = mp.solutions.drawing_utils


while True:
    ret, frame = vide_cam.read()

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (width, height))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hand.HAND_CONNECTIONS)


    cv2.imshow("El Takibi", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vide_cam.release()
cv2.destroyAllWindows()