import os
import shutil
import xml.etree.ElementTree as ET
import random

def mergeContent():
    print("Start merging content...")
    source_folders = [
        "PKLot/PKLot/PUCPR/Sunny",
        "PKLot/PKLot/PUCPR/Cloudy",
        "PKLot/PKLot/PUCPR/Rainy",
        "PKLot/PKLot/UFPR04/Sunny",
        "PKLot/PKLot/UFPR04/Cloudy",
        "PKLot/PKLot/UFPR04/Rainy",
        "PKLot/PKLot/UFPR05/Sunny",
        "PKLot/PKLot/UFPR05/Cloudy",
        "PKLot/PKLot/UFPR05/Rainy"
    ]

    destination_folder = "data/total-content"

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through source folders and merge contents
    for source_folder in source_folders:
        print(f"Processing folder = {source_folder}")
        for root, _, files in os.walk(source_folder):
            for file in files:
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_folder, file)
                shutil.copy(source_file_path, destination_file_path)

    print("Contents merged successfully...\n")


def moveAnnotatedAndXML():
    print("Moving annoted and XML files...")
    input_folder = "data/total-content"
    output_folder = "data/labels-xml"

    image_width = 1280
    image_height = 720

    class_mapping = {"1": 1, "0": 0}

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    xml_files = [f for f in os.listdir(input_folder) if f.endswith(".xml")]
    for xml_file in xml_files:
        xml_path = os.path.join(input_folder, xml_file)
        
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        txt_filename = os.path.splitext(xml_file)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_filename)

        with open(txt_path, "w") as txt_file:
            for space in root.findall("space"):
                occupied = space.get("occupied")
                class_index = class_mapping.get(occupied, -1)
                
                if class_index == -1:
                    continue
                
                rotated_rect = space.find("rotatedRect")
                center = rotated_rect.find("center")
                size = rotated_rect.find("size")
                
                center_x = float(center.get("x"))
                center_y = float(center.get("y"))
                width = float(size.get("w"))
                height = float(size.get("h"))
                
                x_center = center_x / image_width
                y_center = center_y / image_height
                w = width / image_width
                h = height / image_height
                
                txt_file.write(f"{class_index} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
        
        new_xml_path = os.path.join(output_folder, xml_file)
        os.rename(xml_path, new_xml_path)

    print("Annotations generated and XML files moved.\n")

def moveTXTFiles():
    # Move the txt files from the xml folder to the total-content folder
    print("Moving TXT files...")
    source_folder = "data/labels-xml"
    destination_folder = "data/total-content"

    txt_files = [f for f in os.listdir(source_folder) if f.endswith(".txt")]

    for txt_file in txt_files:
        source_path = os.path.join(source_folder, txt_file)
        destination_path = os.path.join(destination_folder, txt_file)
        shutil.move(source_path, destination_path)

    print("TXT files moved to data/total-content folder.\n")

def splitData():
    print("Splitting data...")
    # remove the image that has no corresponding txt file
    file_path = "data/total-content/2012-11-06_18_48_46.jpg"
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been removed successfully.")
    except OSError as e:
        print(f"Error removing the file '{file_path}': {e}")


    source_folder = "data/total-content"
    train_folder = "data/train"
    test_folder = "data/test"
    val_folder = "data/val"

    train_ratio = 0.7
    test_ratio = 0.15

    for folder in [train_folder, test_folder, val_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    all_files = os.listdir(source_folder)
    image_files = [f for f in all_files if f.endswith(".jpg")]

    # Calculate the number of samples for each split
    num_samples = len(image_files)
    num_train = int(train_ratio * num_samples)
    num_test = int(test_ratio * num_samples)

    random.shuffle(image_files)

    train_files = image_files[:num_train]
    test_files = image_files[num_train:num_train + num_test]
    val_files = image_files[num_train + num_test:]

    # Move corresponding txt files along with images
    for folder, files in [(train_folder, train_files), (test_folder, test_files), (val_folder, val_files)]:
        for file in files:
            # Move image file
            source_image_path = os.path.join(source_folder, file)
            destination_image_path = os.path.join(folder, file)
            shutil.move(source_image_path, destination_image_path)
            
            # Move corresponding txt file
            txt_file = os.path.splitext(file)[0] + ".txt"
            source_txt_path = os.path.join(source_folder, txt_file)
            destination_txt_path = os.path.join(folder, txt_file)
            shutil.move(source_txt_path, destination_txt_path)

    print("Data split into train, test, and val sets.\n")


def organizeData():
    datasets = ['train', 'val', 'test']
    source_folder = 'data'

    for dataset in datasets:
        dataset_folder = os.path.join(source_folder, dataset)

        # Create "images" and "labels" folders
        print(f"Create images/ and labels/ for {dataset_folder}")
        images_folder = os.path.join(dataset_folder, "images")
        labels_folder = os.path.join(dataset_folder, "labels")
        os.makedirs(images_folder, exist_ok=True)
        os.makedirs(labels_folder, exist_ok=True)
        print(f"Finish creating images/ and labels/ for {dataset_folder}")

        # Organize image and label files
        print(f"Organizing {dataset_folder}")
        for file in os.listdir(dataset_folder):
            if file.endswith(".jpg"):
                image_path = os.path.join(dataset_folder, file)
                image_destination = os.path.join(images_folder, file)
                shutil.move(image_path, image_destination)
            elif file.endswith(".txt"):
                label_path = os.path.join(dataset_folder, file)
                label_destination = os.path.join(labels_folder, file)
                shutil.move(label_path, label_destination)

    print("Datasets organized successfully.")

if __name__=="__main__": 
    mergeContent() 
    moveAnnotatedAndXML() 
    moveTXTFiles()
    splitData() 
    organizeData()

    # print(f"Size of train folder images = {len(os.listdir('data/train/images'))}")
    # print(f"Size of train folder labels = {len(os.listdir('data/train/labels'))}")

    # print(f"Size of test folder images = {len(os.listdir('data/test/images'))}")
    # print(f"Size of test folder labels = {len(os.listdir('data/test/labels'))}")

    # print(f"Size of val folder images = {len(os.listdir('data/val/images'))}")
    # print(f"Size of val folder labels = {len(os.listdir('data/val/labels'))}")