import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
from datetime import datetime, timedelta
import tensorflow as tf
import requests, json


#// Load model 
# model = tf.keras.models.load_model('rnn_model_3_class_v1.h5')


#// Use docker container:
url = 'http://localhost:8501/v1/models/model_container:predict'
def make_prediction(instances):
   data = json.dumps({"instances": instances.tolist()})
   headers = {"content-type": "application/json"}
   json_response = requests.post(url, data=data, headers=headers)
   predictions = json.loads(json_response.text)['predictions']
   return np.argmax(predictions)


def show_warning_fun(warning_message):
        cv2.rectangle(image, (5,5) , np.array(window_size) - np.array(5), (255,0,0) , 8)
        cv2.putText(image, str(warning_message), (280, 140), font, 3, (255,0,0), 7)


cap = cv2.VideoCapture(0)
window_size = (1280,720)
biceps_bar_counter = 0 
shoulder_wrist_threshold_up = 0
is_shoulder_wrist_up = True
start_time = datetime.now()
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

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.resize(frame, window_size)
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(image)

        # Draw Blacke rectangle:
        cv2.rectangle(image, (0,0) , window_size, (0,0,0) , -1)

        

        more_three_second = start_time + timedelta(seconds=30) #start after ?second
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

                #--------------------------------------------------------
                #------Chick if needs body parts are seen----------------
                #--------------------------------------------------------
                if visibility_thrshould < landmarks[mp_pose.PoseLandmark.NOSE.value].visibility:
                    is_nose_seen = True
                if visibility_thrshould < landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility:
                    is_left_sholder_seen = True
                if visibility_thrshould < landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].visibility:
                    is_left_wrist_seen = True
                if visibility_thrshould < landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility:
                    is_left_hip_seen = True
                if visibility_thrshould < landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility:
                    is_left_elbow_seen = True

                #Chick if all nessery body part are visibale, if yes, do predcation:
                if is_nose_seen and is_left_elbow_seen and is_left_hip_seen and is_left_wrist_seen and is_left_sholder_seen:
                    try:


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



                        
                        # Getting data in one row to make a backage of rows
                        first_sample_counter+=1
                        first_backage_dataset.append(np.array(one_row_of_dataset))



                        #--------------------------------------------------------
                        #---Prediction for every ?? frames---RNN--------
                        #--------------------------------------------------------
                        if first_sample_counter > total_rows_per_package:


                            # Start Predaction
                            predict_data = np.expand_dims(np.array(first_backage_dataset) , axis=0)
                            # print(predict_data.shape)
                            # predicted_value = model.predict(predict_data)
                            #---Predaction From Docker container------
                            predictions = make_prediction(np.expand_dims(predict_data , axis=0))
                            
                            # print(predicted_value)
                            # result_index = np.argmax(predicted_value)
                            result_index = predictions
                            print(f'Predicted Class Label = {result_index} ')



                            # Reset
                            is_nose_seen = False
                            is_left_elbow_seen = False
                            is_left_hip_seen = False
                            is_left_wrist_seen = False
                            is_left_sholder_seen = False
                            # clean dataset backage 
                            first_backage_dataset = []
                            # reset counter to get next 30 dataset for one backage
                            first_sample_counter = 0


                    except:
                        pass

                #--Show warning------
                if result_index == 1 :
                    show_warning_fun('Your arm is up')
                if result_index == 2 :
                    show_warning_fun('Keep Bar lower')

                #--Add one to counter if train is in right way:
                # subtract x,y to get difference and cound total achievements
                shoulder_wrist_diff_y = np.sum(left_wrist[1] - left_shoulder[1])
                shoulder_hip_differ_y = np.sum(left_hip[1] - left_shoulder[1])
                shoulder_visibility = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility
                wrist_visibility = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].visibility

                if (shoulder_wrist_diff_y < int(shoulder_hip_differ_y*.30) + shoulder_wrist_threshold_up) and result_index==0 and is_shoulder_wrist_up:
                    biceps_bar_counter = biceps_bar_counter + 1
                    is_shoulder_wrist_up = False
                if (shoulder_wrist_diff_y > int(shoulder_hip_differ_y*.30) + shoulder_wrist_threshold_up) and result_index==0 and (not is_shoulder_wrist_up):
                    is_shoulder_wrist_up = True

                # cv2.putText(image, str(biceps_bar_counter), (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 100, 0), 4, cv2.LINE_AA)
                cv2.putText(image, str(biceps_bar_counter), (580, 400), font, 8, (255,255,255), 18)
            except:
                pass
        # Truning name
        cv2.putText(image, str('Biceps Bar'), (480, 600), font, 2, (255,255,255), 5)
        # Recolor back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Render detections
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        #                         mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
        #                         mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
        #                          )    



        cv2.imshow('Body Bos', image)


        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()