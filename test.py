from PIL import Image
from ultralytics import YOLO
import os 
import random

def loadModel():
    if not os.path.exists("runs/detect/train/weights/best.pt"):
        raise Exception("You need to train a model first!")
    model = YOLO("runs/detect/train/weights/best.pt")
    return model

def test(model):
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
    result = results[0]
    result.save(filename=f"prediction/result_{random_image}")  # save to disk


if __name__=="__main__": 
    model = loadModel() 
    test(model)