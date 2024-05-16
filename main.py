import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime  

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

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
is_recording = False
video_writer = None

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(image, results.multi_hand_landmarks)
            
            if gesture == "thumbs_up" and not is_recording:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_name = f'recording_{timestamp}.avi'
                print(f"Starting recording: {file_name}")
                is_recording = True
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_writer = cv2.VideoWriter(file_name, fourcc, 20.0, (640, 480))
            
            elif gesture == "thumbs_down" and is_recording:
                print("Stopping recording")
                is_recording = False
                video_writer.release()
    
    if is_recording:
        video_writer.write(frame)
    
    cv2.imshow('Webcam', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
if is_recording:
    video_writer.release()
cv2.destroyAllWindows()