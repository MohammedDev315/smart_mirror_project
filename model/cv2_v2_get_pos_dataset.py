from dataclasses import dataclass
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
from datetime import datetime, timedelta
import json
import copy



def  save_data_to_json(full_json_path , dic_data):
    #---------------------------------------------
    #--- Json file must be created with empty list
    #---------------------------------------------
    print(full_json_path)
    filename = full_json_path
    listObj = []
    
    # Read JSON file
    with open(filename) as fp:
        listObj = json.load(fp)
    
    listObj.append(dic_data)
    
    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file)



cap = cv2.VideoCapture(1)
window_size = (1200,720)
biceps_bar_counter = 0 
shoulder_wrist_threshold_up = 0
is_shoulder_wrist_up = True
start_time = datetime.now()
first_sample_counter = 0
first_backage_dataset = []
second_backage_dataset = []
total_rows_per_package = 29 # start at 0 to ??
visibility_thrshould = 0.70


# training_label = 3 
# training_name  = 'body_move'
# file_name = 'class_3_body_move_datase_4.json' 

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.resize(frame, window_size)
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(image)

        more_three_second = start_time + timedelta(seconds=10) #start after ?second
        if more_three_second < datetime.now():
            try:
                landmarks = results.pose_landmarks.landmark
                # Get lnadmarks
                nose = np.multiply([landmarks[mp_pose.PoseLandmark.NOSE.value].x,landmarks[mp_pose.PoseLandmark.NOSE.value].y], window_size ).astype(int)
                left_shoulder = np.multiply([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y], window_size ).astype(int)
                left_wrist = np.multiply([landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y],window_size).astype(int)
                left_hip = np.multiply([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y],window_size).astype(int)
                left_elbow = np.multiply([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y],window_size).astype(int)
                left_eye = np.multiply([landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y],window_size).astype(int)

                right_shoulder = np.multiply([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y], window_size ).astype(int)
                right_wrist = np.multiply([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y],window_size).astype(int)
                right_hip = np.multiply([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y],window_size).astype(int)
                right_elbow = np.multiply([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y],window_size).astype(int)
                right_eye = np.multiply([landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y],window_size).astype(int)

  

                # Draw rectanle to show them
                cv2.rectangle(image, (nose-10) , (nose+10), (255,255,0) , -1)
                cv2.rectangle(image, (left_shoulder-10) , (left_shoulder+10), (255,255,0) , -1)
                cv2.rectangle(image, (left_wrist-10) , (left_wrist+10), (255,255,0) , -1)
                cv2.rectangle(image, (left_hip-10) , (left_hip+10), (255,255,0) , -1)
                cv2.rectangle(image, (left_elbow-10) , (left_elbow+10), (255,255,0) , -1)




                # Create one row of data for dataset
                one_row_of_dataset = [
                        int(nose[0]),  # 0
                        int(nose[1]), # 1
                        int(left_shoulder[0]), #2 
                        int(left_shoulder[1]), # 3
                        int(left_wrist[0]), # 4
                        int(left_wrist[1]), # 5
                        int(left_hip[0]), # 6
                        int(left_hip[1]), # 7
                        int(left_elbow[0]), # 8
                        int(left_elbow[1]), # 9
                        int(left_eye[0]), # 10
                        int(left_eye[1]), # 11
                        int(right_shoulder[0]), # 12
                        int(right_shoulder[1]), # 13
                        int(right_wrist[0]), # 14
                        int(right_wrist[1]), # 15
                        int(right_hip[0]), # 16
                        int(right_hip[1]), # 17
                        int(right_elbow[0]), # 18
                        int(right_elbow[1]), # 19
                        int(right_eye[0]), # 20
                        int(right_eye[1]) # 21
                    ]

                # Create first general dataset using all data  fro DNN
                # Add dataset DNN to json file
                print(one_row_of_dataset)
                json_file_path = f'./dataset/{file_name}'
                dic_to_be_save  = {
                    "data_rows": one_row_of_dataset,
                    "training_label": int(training_label) , 
                    "training_name" : training_name
                }
                save_data_to_json( json_file_path , dic_to_be_save )

                

            except:
                pass

        # Recolor back to BGR
        # image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )    



        cv2.imshow('Body Bos', image)

        finshing_time = start_time + timedelta(seconds=255) #End after ?second
        if finshing_time < datetime.now():
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()