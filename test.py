from PIL import Image
from ultralytics import YOLO
import os 
import random
import argparse

def loadModel(checkpoint):
    if not os.path.exists(checkpoint):
        raise Exception("The checkpoint doesn't exist. Either you didn't train the model or the path you provided is incorrect.")
    model = YOLO(checkpoint)
    return model

def generateRandomTestImage(): 
    test_directory = "data/test/images"
    image_files = []
    for file in os.listdir(test_directory): 
        if file.lower().endswith(".jpg"):
            image_files.append(file)

    random_image = random.choice(image_files)
    random_image_path = os.path.join(test_directory, random_image)
    return random_image_path

def test(model, test_image):
    # Run the prediction
    if not os.path.exists(test_image):
        raise Exception("The image doesn't exist. Please make sure the path you provided is correct.")
    print(f"Test image = {test_image}")
    results = model.predict(test_image)
    result = results[0]

    # Save the predicted image to disk
    file_name = test_image.split("/")[-1]
    result.save(filename=f"prediction/result_{file_name}") 


if __name__=="__main__": 
    # Generate a randome image for testing if the user doesn't provide anything.
    random_image_path = generateRandomTestImage()

    # Add two command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", help="The pretrained model checkpoint", default="runs/detect/train/weights/best.pt")
    parser.add_argument("--test", help="The path of the test image that you want to run prediction on", default=random_image_path)
    args = parser.parse_args()

    # Load the model from the checkpoint
    model = loadModel(args.ckpt)

    # Run test on the test image
    test(model, args.test)