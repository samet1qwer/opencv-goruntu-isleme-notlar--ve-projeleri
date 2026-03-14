import cv2
import mediapipe as mp

width = 400
height = 400

vide_cam = cv2.VideoCapture(0)

mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh()

mp_draw = mp.solutions.drawing_utils

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

            x_list = []
            y_list = []

            for id , detection in enumerate(face_landmarks.landmark):
                cx , cy = int(detection.x * w), int(detection.y * h)

                x_list.append(cx)
                y_list.append(cy)

                cv2.circle(frame, (cx, cy), 2, (255, 0, 0), cv2.FILLED)

            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0,255,0), 2)

    cv2.imshow("Yuz Tanima", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
vide_cam.release()
cv2.destroyAllWindows()