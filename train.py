from ultralytics import YOLO
import os

def loadModel():
    # Load a model
    if not os.path.exists("yolov8n.pt"):
        model = YOLO("configurations/yolov8.yaml")  # build a new model from YAML
    else:
        model = YOLO("yolov8n.pt")  # load a pretrained model
    return model

if __name__=="__main__":
    # Load the model
    model = loadModel()

    # Train the model
    model.train(data='configurations/data.yaml', epochs=100)