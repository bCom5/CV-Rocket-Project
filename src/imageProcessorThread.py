import io
import time as t
import threading
import picamera
import picamera.array
import Constants
import cv2
import numpy as np
from Filter import Filter as f

# Create a pool of image processors
done = False
frame = 0
numFrames = 500
outputDir = "/home/pi/Documents/RocketProject/cv/src/outputs.txt"
doOutput = False
time = 0
execTime = 0
waits = 0
threadCount = 1
waitDelay = 0.25

lock = threading.Lock()
pool = []

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        # self.stream = picamera.array.PiRGBArray(camera)
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        global done, frame, time, execTime
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    e1 = cv2.getTickCount()
                    self.stream.seek(0)
                    # Read the image and do some processing on it

                    #filt.image = self.stream.array
                    data = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
                    filt.image = cv2.imdecode(data, 1)
                    # ABOVE IS EXPENSIVE - FIND AN ALTERNATIVE

                    filtered, imagey, contours, h = filt.rgbGet(cv2.CHAIN_APPROX_SIMPLE, Constants.VIDEOS_RGB_FILTER_CONSTANTS_1)
                    coolImage = filt.run(filt.image)
                    # Set done to True if you want the script to terminate
                    # at some point
                    #done=True
                    self.stream.truncate()
                    e2 = cv2.getTickCount()
                    execTime = (e2 - e1) / cv2.getTickFrequency()
                    time += execTime
                    frame += 1
                    if frame >= numFrames:
                        done = True
                    print execTime
                # except:
                #     pass
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    e2 = cv2.getTickCount()
                    time += (e2 - e1) / cv2.getTickFrequency()
                    frame += 1
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    global waits
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            # print "WAITING!"
            waits += 1
            waitDelay = execTime + 0.08 #Tries to wait for how long the last run was plus a small buffer. Should not run multiple times, 1 time for one thread
            t.sleep(waitDelay)
            # pass

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(threadCount)]
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.start_preview()
    filt = f(cv2.imread('img/balloon.jpg'), consts=Constants.VIDEOS_CONTOUR_FILTER_CONSTANTS_1, display=False)
    t.sleep(2)
    tot1 = cv2.getTickCount()
    try: 
        camera.capture_sequence(streams(), use_video_port=True)
    except:
        print frame
    tot2 = cv2.getTickCount()
    total = (tot2 - tot1) / cv2.getTickFrequency() # ACCURATE
    cv2.destroyAllWindows()
    camera.close()

    output = "\nTOTAL FILTER TIME:\t "+str(time)+"\n\nAVERAGE TIME PER FRAME:\t "+str(time/numFrames)+"\n\nAVERAGE FRAMES PER SECOND:\t "+str(1 / (time / numFrames))+"\n\nTOTAL TIME INCLUDING CAPTURE:\t "+str(total)+"\n\nAVERAGE TIME PER FRAME INCLUDING CAPTURE:\t "+str(total/numFrames)+"\n\nAVERAGE FRAMES PER SECOND INCLUDING CAPTURE:\t "+str(1 / (total/numFrames))+"\n\nSTOPPED AT FRAME:\t "+str(numFrames)+"\n\nWAITED FOR:\t "+str(waits*(time/numFrames))+" SECONDS!\n\n"
    print output
    if doOutput:
        try:
            fil = open(outputDir, "r")
            fil.close()
        except:
            fil = open(outputDir, "w")
            fil.close()
        f = open(outputDir, "a")
        f.write(output)
        f.write("================================================================")
        f.write("\n\n")
        f.write("================================================================")
        f.close()

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()