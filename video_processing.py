import numpy as np
import cv2 as cv
from ultralytics import YOLO
import os
import argparse

def loadModel(checkpoint):
    if not os.path.exists(checkpoint):
        raise Exception("The checkpoint doesn't exist. Either you didn't train the model or the path you provided is incorrect.")
    model = YOLO(checkpoint)
    return model

def detectEachFrame(model, frame):
    results = model.predict(frame)
    result = results[0]
    return result

def detectParkingSpots():
    model = loadModel("runs/detect/train/weights/best.pt")
    cap = cv.VideoCapture("data/videos/parking1.mp4")

    # We need to set resolutions. 
    # so, convert them from float to integer. 
    frame_width = int(cap.get(3)) 
    frame_height = int(cap.get(4)) 
    fps = cap.get(cv.CAP_PROP_FPS)
    print(f"fps = {fps}")
    
    # Below VideoWriter object will create 
    # a frame of above defined The output  
    # is stored in 'filename.avi' file. 
    # TODO: Figure out how to save mp4 file correctly. 
    # TODO: Get the model to work on the video correctly. 
    # result = cv.VideoWriter('prediction/videos/parkingspot.mp4',  
    #                         cv.VideoWriter_fourcc(*'mp4v'), 
    #                         fps, (1080, 1920)) 
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        detected_frame = detectEachFrame(model, frame)
        detected_frame.save(filename=f"prediction/videos/train/save_{count}.png")
        count += 1
        
        # Save as a video
        # detected_frame = detected_frame.plot()
        # detected_frame = cv.cvtColor(detected_frame, cv.COLOR_BGR2RGB)
        # print(f"Type = {type(detected_frame)}, Shape = {detected_frame.shape}")
        # result.write(detected_frame)

        # if cv.waitKey(10) == ord('q'):
        #     break

    cap.release()
    # result.release()
    # cv.destroyAllWindows()

if __name__=="__main__":
    detectParkingSpots()