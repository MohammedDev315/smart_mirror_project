import cv2
import time
import numpy as np 
start = time.time()

label = 2
rand = np.random.randint(999)
time.sleep(3)
for idx in range(3):
    time.sleep(3)
    video = cv2.VideoCapture(0)
    if (video.isOpened() == False):
        print("Error reading video file")
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    size = (frame_width, frame_height)
    result = cv2.VideoWriter(f'dataset/biceps_dumbbell2/label_{label}_v_{idx}_g_{rand}.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, size)
    count = 0
    while(True):
        ret, frame = video.read()
        count += 1
        if ret == True:
            result.write(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
            
            if count == 150 :
                break
            
        # Break the loop
        else:
            break


    video.release()
    result.release()
    cv2.destroyAllWindows()
    print("The video was successfully saved")