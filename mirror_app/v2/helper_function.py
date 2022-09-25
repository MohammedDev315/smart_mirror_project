import numpy as np
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import requests
import base64
import json   
import ssl
import requests
ssl._create_default_https_context = ssl._create_unverified_context

dumbbell_model = tf.keras.models.load_model('LRCN_model_22f_v_1.h5')
biceps_barbel_model = tf.keras.models.load_model('biceps_bar_40f_v1.1.h5')
api = 'http://127.0.0.1:5000/test'
model = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
movenet = model.signatures['serving_default']


body_part = ['nose', 'left eye', 'right eye', 'left ear', 'right ear', 'left shoulder', 'right shoulder', 'left elbow', 'right elbow', 'left wrist', 'right wrist', 'left hip', 'right hip', 'left knee', 'right knee', 'left ankle', 'right ankle']
pose_model_image_size = 192
visibility_threshold = .30
DUMBBELL_MODEL_SEQUENCE_LENGTH = 22
biceps_counter_threshold = 65 # less is more accureate and hard to get
right_wrist_visibility_threshold = 35 # in persentage



def get_pose(frame):
  body_pose = {}
  #-- Select an image
  image = np.array(frame)
  image = tf.expand_dims(image, axis=0)
  image = tf.cast(tf.image.resize_with_pad(image, pose_model_image_size, pose_model_image_size), dtype=tf.int32)
  # Run model inference.
  outputs = movenet(image)
  keypoints = outputs['output_0']
  keypoints = keypoints[0][0]
  #===== Getting x , y  ==========
  for selected_part in range(17):
    part = np.array(np.array(keypoints[selected_part] , dtype=np.float32) , dtype=np.float32)
    visibility = part[2]
    if visibility > visibility_threshold:  
      body_pose[ body_part[selected_part] ] =  [part[1], part[0], part[2] ]  #covert y,x to x,y 
    else:
      body_pose[ body_part[selected_part] ] =  [ 0, 0, 0 ] 
  return body_pose


def get_user_data_fun(frame, current_user_data):
    #===========================================================
    #--Crop only face from image
    # face_cropped = crop_imgage('nose', frame, ORGINAL_IMAGE_WIDTH, ORGINAL_IMAGE_HEIGHT, body_pose, 500, 400)
    #--Get user data from database by using his/her name
    face_frame = frame # or we can use Cropped image
    face_frame = cv2.cvtColor(np.array(face_frame), cv2.COLOR_BGR2RGB)
    face_frame = cv2.resize(face_frame, (300, 200))
    _, img_encoded = cv2.imencode('.jpeg', face_frame)

    im_b64 = base64.b64encode(np.array(img_encoded)).decode("utf8")

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    payload = json.dumps({"image": im_b64, "other_key": "value"})
    response = requests.post(api, data=payload, headers=headers)
    try:
        current_user_data = response.json()            
    except requests.exceptions.RequestException:
        print(response.text)

    return current_user_data



def get_user_exercise_plan(user_id):
    r = requests.post('http://192.168.8.181:5006/get_excercise_plan', json={"uid": f"{user_id}"})
    r.json()
    dd = r.json()
    dd = dd['data']
    trining_list = [] 
    if dd['exr1'] != None:
        trining_list.append({ 'exrid' : dd['exr1']['exrid'] , 'is_done' : dd['done1']  })
    if dd['exr2'] != None:
        trining_list.append({ 'exrid' : dd['exr2']['exrid'] , 'is_done' : dd['done2']  })
    if dd['exr3'] != None:
        trining_list.append({ 'exrid' : dd['exr3']['exrid'] , 'is_done' : dd['done3']  })
    if dd['exr4'] != None:
        trining_list.append({ 'exrid' : dd['exr4']['exrid'] , 'is_done' : dd['done4']  })
    #---Get first exercise id that has not done yet:
    selected_id = 0 
    for x in trining_list:
        if x['is_done'] == False:
            print(x)
            selected_id = x['exrid']
            break
    return selected_id



def crop_imgage(selected_body_part, frame, frame_width, frame_hight, body_pose, cropped_width, corpped_hight):
    selected_part = (np.array(body_pose[selected_body_part])*[frame_width , frame_hight , 100]).astype(int)
    # Cropping image
    try:
        frame = tf.image.crop_to_bounding_box( np.array(frame), selected_part[1] - int(cropped_width/2), selected_part[0]- int(corpped_hight/2), cropped_width, corpped_hight )
    except:
        frame = tf.zeros([cropped_width, corpped_hight , 3], tf.int32)
    return frame



def dumbbells_model_prediction(frame , body_pose, tem_frames, frames_list, dumbbells_prediction_result):
    #--corp image and get right wrist for dumbbellls model
    #--size  of image must be 200 * 200 and the crop resutl will be 80*80 as model ask
    frame_for_dumbbell_model = cv2.resize(frame, (200, 200))
    frame_for_dumbbell_model = cv2.cvtColor(frame_for_dumbbell_model, cv2.COLOR_BGR2RGB)
    right_wrist_cropped = crop_imgage('right wrist', frame_for_dumbbell_model, 200, 200, body_pose, 80, 80)
    #--Normaillized data----
    if np.array(right_wrist_cropped).ndim == 3:
        tem_frames.append(right_wrist_cropped / 255)
    else:
        print('Frame not added')
    #--Start Predect-------
    if len(tem_frames) == DUMBBELL_MODEL_SEQUENCE_LENGTH: 
        frames_list.append(tem_frames)
        prediction_result = dumbbell_model.predict(np.array(frames_list))
        dumbbells_prediction_result = np.argmax(prediction_result)
        tem_frames = []
        frames_list = []
    return tem_frames, frames_list, dumbbells_prediction_result




def biceps_counter_function(is_model_result_green, body_pose, biceps_counter, is_able_to_increase_biceps_counter ):
    right_wrist = (np.array(body_pose['right wrist'])*[600,600,100]).astype(int)
    right_shoulder = (np.array(body_pose['right shoulder'])*[600,600,100]).astype(int)
    right_hip= (np.array(body_pose['right hip'])*[600,600,100]).astype(int)
    right_shoulder_wrist_diff  = np.absolute(((right_shoulder[1] - right_wrist[1])*(100/ ( right_hip[1] - right_shoulder[1] ) )).astype(int))
    print(right_shoulder_wrist_diff)
    print(is_model_result_green)
    if (right_shoulder_wrist_diff < biceps_counter_threshold) and (right_wrist[2] > right_wrist_visibility_threshold) and is_model_result_green  :
        if is_able_to_increase_biceps_counter:
            biceps_counter  += 1
            is_able_to_increase_biceps_counter = False
    if (right_shoulder_wrist_diff > biceps_counter_threshold) and (right_wrist[2] > right_wrist_visibility_threshold)  :
        is_able_to_increase_biceps_counter = True
    return biceps_counter, is_able_to_increase_biceps_counter



def biceps_barbell_model_prediction(frame , tem_frames, frames_list , biceps_barbell_prediction_result ):
    SEQUENCE_LENGTH = 40
    frame = cv2.resize(frame, (int(1280/4), int(720/4)))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    normalized_frame = frame / 255
    tem_frames.append(normalized_frame)

    if len(tem_frames) == SEQUENCE_LENGTH: 
        frames_list.append(tem_frames)
        print(np.array(frames_list).shape)
        biceps_barbell_prediction_result = biceps_barbel_model.predict(np.array(frames_list))
        biceps_barbell_prediction_result = np.argmax(biceps_barbell_prediction_result)
        tem_frames = []
        frames_list = []

    return tem_frames, frames_list, biceps_barbell_prediction_result





def train_mirror_messages(frame, counter, train_name, message_type, message ,frame_w  , frame_h ):
    frame_size = (frame_w,frame_h)
    warning_message = message
    if message_type == 'warning':
        cv2.rectangle(frame, (5,5) , np.array(frame_size) - np.array(15), (0,0,255) , 20)
        cv2.putText(frame, str(warning_message), (280, 140), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 7)
    cv2.putText(frame, str(counter), (580, 400), cv2.FONT_HERSHEY_SIMPLEX, 8, (255,255,255), 18)
    cv2.putText(frame, str(train_name), (480, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5)
    return frame 



def text_mirror_message(frame, message, message_header):
    cv2.putText(frame, str(message_header), (380, 240), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 7)
    cv2.putText(frame, str(message), (120, 440), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 7)
    cv2.imshow('frame', frame)
    return frame 










