from PIL import Image
from ultralytics import YOLO
import os 
import random

def loadModel():
    if not os.path.exists("yolov8n.pt"):
        raise Exception("You need to train a model first!")
    model = YOLO("yolov8n.pt")
    return model

def test(model):
    # TODO: Figure out how to test the model using only 2 classes. 
    test_directory = "data/test/images"
    image_files = []
    for file in os.listdir(test_directory): 
        if file.lower().endswith(".jpg"):
            image_files.append(file)

    random_image = random.choice(image_files)
    random_image_path = os.path.join(test_directory, random_image)

    # Run the prediction
    print(f"Random image = {random_image}")
    results = model.predict(random_image_path)
    print(f"Results = {results}")
    # Process results list
    result = results[0]
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    result.save(filename=f"result_{random_image}")  # save to disk


if __name__=="__main__": 
    model = loadModel() 
    test(model)