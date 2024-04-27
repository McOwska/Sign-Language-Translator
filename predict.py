import os
import numpy as np
import cv2
import mediapipe as mp
from itertools import product
import keyboard
from expressions import lesson_1, lesson_2, lesson_3, lesson_4
from tensorflow.keras.models import load_model
model = load_model('my_model_3_1.keras')

def extract_keypoints(results):
    keypoints = np.array([])
    for landmark_list in [results.left_hand_landmarks, results.right_hand_landmarks]:
        if landmark_list is not None:
            for landmark in landmark_list.landmark:
                keypoints = np.append(keypoints, [landmark.x, landmark.y, landmark.z])
        else:
            #  when there are no keypoints detected
            keypoints = np.append(keypoints, np.zeros(21*3)) 
    return keypoints

def process_image_and_predict(cap, holistic, model, actions):
    success, image = cap.read()
    if not success:
        print("Failed to capture image.")
        return None, None

    image = cv2.flip(image, 1)  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = holistic.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    mp.solutions.drawing_utils.draw_landmarks(image, results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
    mp.solutions.drawing_utils.draw_landmarks(image, results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)

    keypoints = extract_keypoints(results)
    if keypoints.size > 0:  # Check if keypoints array is not empty
        keypoints = np.array([keypoints])
        prediction = model.predict(keypoints)
        predicted_action = np.argmax(prediction)
        confidence = np.max(prediction)
        return image, f"Predicted Action: {actions[predicted_action]} with confidence: {confidence:.2f}"
    return image, None

def main():
    actions = []
    for i in range(1, 3):
        actions.append(f'lesson_{i}')
        
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot access camera.")
        return

    with mp.solutions.holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75) as holistic:
        while True:
            image, prediction = process_image_and_predict(cap, holistic, model, actions)
            if image is not None:
                cv2.imshow('Camera', image)
                if prediction:
                    print(prediction)
            
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):  # Press 'q' to quit
                break
            if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
