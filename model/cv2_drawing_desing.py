from cgi import print_arguments
from dataclasses import dataclass
from statistics import mode
from tkinter.tix import Tree
import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
window_size = (1280,720)
first_sample_counter = 0
first_backage_dataset = []
second_backage_dataset = []
total_rows_per_package = 59 # start at 0 to ?? frams per backage
visibility_thrshould = 0.70
is_nose_seen = False
is_left_elbow_seen = False
is_left_hip_seen = False
is_left_wrist_seen = False
is_left_sholder_seen = False
font = cv2.FONT_HERSHEY_SIMPLEX
result_index = 0

while cap.isOpened():
    ret, frame = cap.read()
    image = cv2.resize(frame, window_size)
    # Draw Blacke rectangle:
    cv2.rectangle(image, (0,0) , window_size, (0,0,0) , -1)
    # Writing warning message
    warning_message = 'Your arm is up'
    warning_message = 'Keep Bar lower'
    # cv2.rectangle(image, (5,5) , np.array(window_size) - np.array(5), (0,0,255) , 8)
    # cv2.putText(image, str(warning_message), (280, 140), font, 3, (0,0,255), 7)
    cv2.putText(image, str(1), (580, 400), font, 8, (255,255,255), 18)
    cv2.putText(image, str('Biceps Bar'), (480, 600), font, 2, (255,255,255), 5)



    cv2.imshow('Body Bos', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()