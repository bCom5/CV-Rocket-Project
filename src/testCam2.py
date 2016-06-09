import numpy as np
import cv2

cap = cv2.VideoCapture(0)
frames = 0

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(-1)
fourcc = cv2.VideoWriter_fourcc(*'raw ')
out = cv2.VideoWriter('vid/output.mov',fourcc, 15.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        frames += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print frames
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()