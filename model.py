import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from itertools import product
from sklearn import metrics

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

from tensorflow.keras.callbacks import TensorBoard
import datetime
log_dir = os.path.join('logs', 'fit', datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
print(log_dir)
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

PATH = os.path.join('data')

actions = np.array(os.listdir(PATH))

label_map = {label:num for num, label in enumerate(actions)}

landmarks, labels = [], []

for action in actions:
    action_path = os.path.join(PATH, action)
    
    sequences = os.listdir(action_path)

    for sequence in sequences:
        temp = []
        sequence_path = os.path.join(action_path, sequence)
        
        frames = sorted(os.listdir(sequence_path)) 
        
        for frame in frames:
            npy_path = os.path.join(sequence_path, frame)
            if os.path.isfile(npy_path):
                npy = np.load(npy_path)
                temp.append(npy)
        
        if temp:
            landmarks.append(temp)
            labels.append(label_map[action])

X, Y = np.array(landmarks), to_categorical(labels).astype(int)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10, random_state=34, stratify=Y)

model = Sequential()
model.add(LSTM(32, return_sequences=True, activation='relu', input_shape=(10,126)))
model.add(LSTM(64, return_sequences=True, activation='relu'))
model.add(LSTM(32, return_sequences=False, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(X_train, Y_train, epochs=100, callbacks=[tensorboard_callback])

model.save('my_model.keras')

predictions = np.argmax(model.predict(X_test), axis=1)
test_labels = np.argmax(Y_test, axis=1)

accuracy = metrics.accuracy_score(test_labels, predictions)
