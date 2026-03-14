import cv2
import mediapipe as mp
import math

def calculate_angle(a, b, c):
   
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - \
              math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(math.degrees(radians))
    if angle > 180:
        angle = 360 - angle
    return angle

video = cv2.VideoCapture("video.mp4")

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

rep_count = 0
stage = None

ANGLE_UP = 130     
ANGLE_DOWN = 160   

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        h, w, c = frame.shape
        lms = results.pose_landmarks.landmark

        def get_point(idx):
            lm = lms[idx]
            return (int(lm.x * w), int(lm.y * h))

        left_shoulder = get_point(11)
        left_elbow    = get_point(13)
        left_wrist    = get_point(15)
        right_shoulder = get_point(12)
        right_elbow    = get_point(14)
        right_wrist    = get_point(16)

        left_angle  = calculate_angle(left_shoulder,  left_elbow,  left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        avg_angle = (left_angle + right_angle) / 2
        cv2.putText(frame, f"{int(left_angle)}",
                    (left_elbow[0] - 40, left_elbow[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"{int(right_angle)}",
                    (right_elbow[0] + 10, right_elbow[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        if avg_angle < ANGLE_UP:
            stage = "up"
        elif avg_angle > ANGLE_DOWN and stage == "up":
            stage = "down"
            rep_count += 1
        cv2.rectangle(frame, (0, 0), (300, 90), (0, 0, 0), cv2.FILLED)
        cv2.putText(frame, f"Tekrar: {rep_count}", (10, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)
        cv2.putText(frame, f"Asama: {stage if stage else '-'}  Aci: {int(avg_angle)}", (10, 78),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Sayac", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()