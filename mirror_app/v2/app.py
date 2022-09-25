import time
import cv2
import numpy as np
from helper_function import * 



frames_list = []
tem_frames = []
ORGINAL_IMAGE_WIDTH = 1440
ORGINAL_IMAGE_HEIGHT = 900
current_user_data = {}
current_user_data['uid'] = 0
selected_exercise_id = 0
dumbbells_prediction_result  = -1
biceps_barbell_prediction_result = -1
biceps_counter = 0
is_able_to_increase_biceps_counter = True
is_model_result_green = False
message_type   = ''
message = ''




vid = cv2.VideoCapture(0)
while(True):
    ret, frame = vid.read()
    orginal_frame = cv2.resize(frame, (ORGINAL_IMAGE_WIDTH, ORGINAL_IMAGE_HEIGHT))
    cv2.rectangle(orginal_frame, (0,0) , ( ORGINAL_IMAGE_WIDTH, ORGINAL_IMAGE_HEIGHT )  , (0,0,0) , -1)

    
    #--Getting pose of all body parts
    body_pose = get_pose(frame)



    #--Getting user data if mirror not reserved
    if current_user_data['uid'] <= 0 :
       current_user_data =  get_user_data_fun(frame, current_user_data)
       print(current_user_data)
    #    if current_user_data['uid'] > 0 : 
    #        orginal_frame = text_mirror_message(frame, current_user_data['fullname'], 'Welcome')
    #        cv2.imshow('frame', orginal_frame) # to show message on screen befor sleeping
    #        time.sleep(2)



    #--Getting exercises and their data from database-------
    if current_user_data['uid'] > 0 and selected_exercise_id == 0: # I did exercise == 0 to colse request when we get an exercise id, so, after the selected exercise done, we can return it back to 0 and get next exercise
        selected_exercise_id = get_user_exercise_plan(current_user_data['uid'])
        print(selected_exercise_id)


    #--Chekking hammer biceps exercise -----
    if current_user_data['uid'] > 0 and selected_exercise_id == 6:
        #--Reset biceps_barbell_prediction_result to get new result
        biceps_barbell_prediction_result  = -1
        #--pass all necessary data  to dumbbells model to get prediction
        tem_frames, frames_list, biceps_barbell_prediction_result = biceps_barbell_model_prediction(frame ,  tem_frames, frames_list, biceps_barbell_prediction_result )
        if biceps_barbell_prediction_result > -1 :
            if biceps_barbell_prediction_result == 0 or biceps_barbell_prediction_result == 2 :
                is_model_result_green = True
                message_type = 'success'
            else:
                is_model_result_green = False
                message_type = 'warning'
                message = 'Keey your hand colse'

        print(f"Biceps =={biceps_barbell_prediction_result}====")
        #--Change message on screen 
        orginal_frame = train_mirror_messages(orginal_frame, biceps_counter, "Biceps Bar", message_type , message , ORGINAL_IMAGE_WIDTH, ORGINAL_IMAGE_HEIGHT )
        #--Count how many biceps round done?
        biceps_counter, is_able_to_increase_biceps_counter = biceps_counter_function(is_model_result_green, body_pose, biceps_counter, is_able_to_increase_biceps_counter )
        print(f"=======> Counter  : {biceps_counter}")
        #--when counter reached 12 round
        if biceps_counter >5:
            current_user_data['uid'] = 0
            selected_exercise_id = 0 
            biceps_counter = 0 
            frames_list = []
            tem_frames = []
            # time.sleep(5)




    #--Chekking hammer biceps exercise -----
    if current_user_data['uid'] > 0 and selected_exercise_id == 5:

        #--Reset dumbbells_prediction_result to get new result
        dumbbells_prediction_result  = -1
        #--pass all necessary data  to dumbbells model to get prediction
        tem_frames, frames_list, dumbbells_prediction_result = dumbbells_model_prediction(frame , body_pose, tem_frames, frames_list, dumbbells_prediction_result )
        if dumbbells_prediction_result > -1 :
            print(f"Welcome {current_user_data['fullname']} ")
            print(f"Biceps Hammer=={dumbbells_prediction_result}====")
            if dumbbells_prediction_result == 0:
                is_model_result_green = True
                message_type = 'success'
            else:
                is_model_result_green = False
                message_type = 'warning'
                if dumbbells_prediction_result == 1:
                    message = 'Do it as Hummer'
                if dumbbells_prediction_result == 2:
                    message = 'Do it as Hummer'
        #--Change message on screen 
        orginal_frame = train_mirror_messages(orginal_frame, biceps_counter, "Biceps Hammer", message_type , message , ORGINAL_IMAGE_WIDTH, ORGINAL_IMAGE_HEIGHT )
        #--Count how many biceps round done?
        biceps_counter, is_able_to_increase_biceps_counter = biceps_counter_function(is_model_result_green, body_pose, biceps_counter, is_able_to_increase_biceps_counter )
        print(f"=======> Counter  : {biceps_counter}")
        #--when counter reached 12 round
        if biceps_counter >5:
            orginal_frame = text_mirror_message(frame, current_user_data['fullname'], 'You Are Done')
            current_user_data['uid'] = 0
            selected_exercise_id = 0 
            biceps_counter = 0 
            frames_list = []
            tem_frames = []
            # time.sleep(5)




    #===========================================================
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
    cv2.imshow('frame', orginal_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
