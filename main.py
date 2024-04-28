# %%

# Import necessary libraries
import numpy as np
import os
import string
import mediapipe as mp
import cv2
from my_functions import *
import keyboard
from tensorflow.keras.models import load_model
from collections import deque
import json


def process_image_and_extract_keypoints(cap, holistic):
    success, image = cap.read()
    if not success:
        print("Failed to capture image.")
        return False

    image = cv2.flip(image, 1)  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = holistic.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # draw landmarks
    mp.solutions.drawing_utils.draw_landmarks(image, results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
    mp.solutions.drawing_utils.draw_landmarks(image, results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
    
    keypoints = extract_keypoints(results)
    
    return image, keypoints

# Extracting keypoints
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

PATH = os.path.join('data')

with open('labels_my_model_4.json', 'r') as f:
    label_map = json.load(f)
    
actions = np.array(list(label_map.keys()))

model = load_model('my_model_4_3.keras')

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot access camera.")
    exit()

def main():
    with mp.solutions.holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75) as holistic:
        while cap.isOpened():
            
            image, keypoint = process_image_and_extract_keypoints(cap, holistic)
            cv2.imshow('Camera', image)
            
            print("Press SPACE to recognize the action.")
            while not keyboard.is_pressed('space'):
                image, keypoint = process_image_and_extract_keypoints(cap, holistic)
                cv2.imshow('Camera', image)
                
                if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
                        cap.release()
                        cv2.destroyAllWindows()
                        return
            keypoints = deque(maxlen=30)
            print("Recognizing the action....") 
            while len(keypoints) < 30:
                image, keypoint = process_image_and_extract_keypoints(cap, holistic)
                print(len(keypoints))
                cv2.imshow('Camera', image)
                keypoints.append(keypoint)
                if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
                        cap.release()
                        cv2.destroyAllWindows()
                        return   
                                      
            keypoints_array = np.array(keypoints)
            prediction = model.predict(keypoints_array[np.newaxis, :, :])
            keypoints = []  
            if np.amax(prediction) > 0.1:
                predicted_index = np.argmax(prediction)
                predicted_action = actions[predicted_index]
                print(f"Recognized action: {predicted_action} with confidence: {np.max(prediction):.2f}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()
