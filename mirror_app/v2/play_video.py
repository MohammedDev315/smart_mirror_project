
import cv2
 
 
# cap = cv2.VideoCapture('dataset/biceps_dumbbell /class_one/class_1_v_1.mp4')
cap = cv2.VideoCapture('dataset/biceps_dumbbell2/label_0_v_1_g_532.avi')
count = 0 
 
#myvid.avi
 
while(cap.isOpened()):
    ret, frame = cap.read()
 
    count+=1
    print(count)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)
 
 
    if cv2.waitKey(1) == ord('q'):
        break
 
 
cap.release()
cv2.destroyAllWindows()