from flask import Flask
from flask_cors import CORS
from flask import Flask , jsonify , request
import requests
import io
import json                    
import base64                  
import logging             
import numpy as np
from PIL import Image
import face_recognition
import cv2
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import psycopg2


app = Flask(__name__)
CORS(app)


# Connect to your postgres DB
# 192.168.8.188 my computer ip on network
#  port 5433 is written durange docker creation.
# dbname='postgres' is the name of database which created dureing contaner creation not a container name
conn = psycopg2.connect(" dbname='postgres' host='192.168.8.181' port=5434  user='postgres' password='pass'  ")
cur = conn.cursor()


query = 'select * from users'
cur.execute(query)
records = cur.fetchall()
users_list =[]
for user in records:
    users_list.append({
        'uid' : user[0],
        'fullname' : user[1],
        'email' : user[2],
        'image_url' : user[4]
    })
print(users_list)






jev_basses = face_recognition.load_image_file('img2.jpeg')
jev_basses_encoding = face_recognition.face_encodings(jev_basses)[0]

jobs_images = face_recognition.load_image_file('img1.jpeg')
jobs_images_encoding = face_recognition.face_encodings(jobs_images)[0]


response_taylor_swift = urllib.request.urlopen('http://2.bp.blogspot.com/-tYeBnQm3Vg8/UZIAxBnDmfI/AAAAAAAAAJI/7x59qshWmhk/s1600/taylor_swift_png_by_speaknowtutorials-d4lxzih.png')
image_taylor_swift = face_recognition.load_image_file(response_taylor_swift)
taylor_swift_encoding = face_recognition.face_encodings(image_taylor_swift)[0]


known_face_encoding = [
    jev_basses_encoding , 
    jobs_images_encoding,
    taylor_swift_encoding
]

known_face_names=[
    "jev",
    "jobs" , 
    'taylor swift',
]


for user in users_list:
    image = urllib.request.urlopen(user['image_url'])
    image = face_recognition.load_image_file(image)
    image_encoding = face_recognition.face_encodings(image)[0]
    known_face_encoding.append(image_encoding)
    known_face_names.append(user)




@app.route("/test", methods=['POST'])
def test_method():         
    # print(request.json)      
    if not request.json or 'image' not in request.json: 
        # abort(400)
        print('400')
             
    # get the base64 encoded string
    im_b64 = request.json['image']

    # convert it into bytes  
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))
  

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))

    # PIL image object to numpy array
    img_arr = np.asarray(img)      
    print('img shape', img_arr.shape)
    


    face_locations = face_recognition.face_locations(img_arr)
    face_encodings = face_recognition.face_encodings(img_arr, face_locations) 
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
        result=""
        face_distance = face_recognition.face_distance(known_face_encoding, face_encoding) 
        best_match_index = np.argmin(face_distance) 
        if matches[best_match_index] :
            result  = known_face_names[best_match_index]
        else:
            print("Not found")

    return result
  


if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0")


# docker build --tag flask-as-server-image .
# docker run -d -p 5008:5000 --name flask-as-server-container flask-as-server-image