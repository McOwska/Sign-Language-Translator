import os
import numpy as np
import cv2
import mediapipe as mp
from itertools import product
import keyboard
from expressions import lesson_1, lesson_2, lesson_3, lesson_4

# Create directories to save the recorded training data
def prepare_dataset_directory(actions, sequences, path):
    for action, sequence in product(actions, range(sequences)):
        os.makedirs(os.path.join(path, action, str(sequence)), exist_ok=True)

# Extracting keypoints and saving them to a file
def process_image_and_extract_keypoints(cap, holistic, action, sequence, frame, path):
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

    # saving keypoints
    if frame is not None:
        keypoints = extract_keypoints(results)
        np.save(os.path.join(path, action, str(sequence), str(frame)), keypoints)

    return image

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


def main():
    actions = np.array(lesson_1)
    sequences = 30
    frames = 30
    PATH = 'data'

    prepare_dataset_directory(actions, sequences, PATH)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot access camera.")
        return

    with mp.solutions.holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75) as holistic:
        for action in actions:
            flag = 0
            for sequence in range(sequences):
                print(f"Collecting data for: {action} sequence no: {sequence}.")
                if flag != 0:
                    break
                for frame in range(frames):
                    if frame == 0:
                        while not keyboard.is_pressed(' '):
                            image = process_image_and_extract_keypoints(cap, holistic, action, sequence, None, PATH)
                            cv2.imshow('Camera', image)
                            if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
                                cap.release()
                                cv2.destroyAllWindows()
                                return
                            if keyboard.is_pressed('right'):
                                flag += 1
                                break
                    if flag != 0:
                        break
                    print(f"Collecting frames. Action: {action} frame no: {frame}")
                    image = process_image_and_extract_keypoints(cap, holistic, action, sequence, frame, PATH)
                    cv2.imshow('Camera', image)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
