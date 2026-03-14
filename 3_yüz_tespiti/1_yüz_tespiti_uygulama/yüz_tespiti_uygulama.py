import cv2
import mediapipe as mp
import math

width = 400
height = 400

vide_cam = cv2.VideoCapture(0)

mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh()

mp_draw = mp.solutions.drawing_utils

blink_count = 0
blink_state = False

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

while True:
    ret , frame = vide_cam.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (width, height))
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face.process(frame_rgb)
    
    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:

            mp_draw.draw_landmarks(
                frame,
                face_landmarks,
                mp_face.FACEMESH_CONTOURS
            )

            h, w, c = frame.shape

            points = {}

            for id , lm in enumerate(face_landmarks.landmark):

                if id in [33,133,159,145]:

                    cx , cy = int(lm.x * w), int(lm.y * h)

                    points[id] = (cx,cy)

                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)

            if len(points) == 4:

                horizontal = distance(points[33],points[133])
                vertical = distance(points[159],points[145])

                ear = vertical / horizontal

                if ear < 0.2 and blink_state == False:
                    blink_count += 1
                    blink_state = True

                if ear > 0.25:
                    blink_state = False

    cv2.putText(frame,f"Blinks: {blink_count}",(20,60),
                cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),3)

    cv2.imshow("Blink Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
vide_cam.release()
cv2.destroyAllWindows()