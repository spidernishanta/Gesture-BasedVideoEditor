import cv2
import mediapipe as mp
import json
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

gesture_log = []  
recording_start_time = time.time()  

def detect_gesture(image, hand_landmarks, hand_no=0):
    if hand_landmarks:
        landmarks = hand_landmarks[hand_no].landmark
        thumb_tip = landmarks[4]
        thumb_base = landmarks[2]
        if thumb_tip.y < thumb_base.y:
            return "thumbs_up"
        else:
            return "thumbs_down"
    return None

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(image, results.multi_hand_landmarks)
            if gesture:
                current_time = time.time() - recording_start_time  
                gesture_log.append({"gesture": gesture, "timestamp": current_time})
                print(f"Gesture {gesture} detected at {current_time:.2f} seconds")

    cv2.imshow('Webcam', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

with open('gesture_log.json', 'w') as f:
    json.dump(gesture_log, f)