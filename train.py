from ultralytics import YOLO
import os
import argparse

def loadModel():
    # Load a model
    if not os.path.exists("yolov8n.pt"):
        model = YOLO("configurations/yolov8.yaml")  # build a new model from YAML
    else:
        model = YOLO("yolov8n.pt")  # load a pretrained model
    return model

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", help="The number of epochs to train the model", default=50, type=int)
    args = parser.parse_args()

    # Load the model
    model = loadModel()

    # Train the model
    model.train(data='configurations/data.yaml', epochs=args.epochs)