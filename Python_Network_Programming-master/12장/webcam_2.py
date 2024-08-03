import numpy as np
import cv2

cap = cv2.VideoCapture('rtsp://127.0.0.1:8000')

while(True):

    ret, frame = cap.read()
    cv2.imshow('Stream IP camera opencv',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()