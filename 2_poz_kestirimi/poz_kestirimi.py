import cv2
import mediapipe as mp

width = 400
height = 400

vide_cam = cv2.VideoCapture(0)

mp_pozition = mp.solutions.pose
pose = mp_pozition.Pose()

mp_draw = mp.solutions.drawing_utils

while True:
    ret , frame = vide_cam.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = pose.process(frame_rgb)
    
    if result.pose_landmarks:
        mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pozition.POSE_CONNECTIONS)
        for id , lm in enumerate(result.pose_landmarks.landmark):
            h, w, c = frame.shape
            cx , cy = int(lm.x * w), int(lm.y * h)
            print(id, lm)
            if id == 0:
                cv2.circle(frame, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
    
    
    cv2.imshow("poz kestirimi", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
vide_cam.release()
cv2.destroyAllWindows()
