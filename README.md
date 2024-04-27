# Parking Spot Detection Using YOLOv8

## Description

A Parking spot detection built based on YOLOv8, a state-of-the-art object detection model. 

## Getting Started

### Dependencies

* This project requires Python 3.8+ and CUDA 12+.  

### Installing

* Create a conda environment and activate it. 
```
conda create --name parkingspot
conda activate parkingspot
```
* Install all required libraries
```
pip install -r requirements.txt
```

### Dataset

* This project uses a parking lot dataset from Kaggle. This dataset consists of 12000 images captured at a parking lot in various weather conditions and camera angles. The dataset can be downloaded here: https://www.kaggle.com/datasets/blanderbuss/parking-lot-dataset 
* After unzip the folder, preprocess the dataset and split it into training, validation and testing folders. 
```
python data_preprocessing.py
```

### Train the model

* Run the following command to train the model. If you don't provide the number of trained epochs, the default value is 50. 
```
python train.py --epochs=<your_epochs>
```

### Test the model on an image

* Run the following command to test the model on a single image. The default checkpoint is in runs/train4 and the default tested image is randomly selected from the test set.  
```
python test.py --ckpt=<your_checkpoint> --test=<path_to_image>
```

### Test the model on a video

* Run the following command to test the model on a single video. The video is provided in data/videos folder. 
```
python video_processing.py
```