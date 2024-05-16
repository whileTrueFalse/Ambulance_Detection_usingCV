HANDS ON PROJECT GUIDE & SETUP
This guide explains how to train your own custom dataset with YOLOv5 🚀.

Before You Start
Clone repo and install requirements.txt in a Python>=3.8.0 environment, including PyTorch>=1.8. Models and datasets download automatically from the latest YOLOv5 release.


git clone https://github.com/ultralytics/yolov5  # clone
cd yolov5
pip install -r requirements.txt  # install
Train On Custom Data
Ultralytics active learning


Creating a custom model to detect your objects is an iterative process of collecting and organizing images, labeling your objects of interest, training a model, deploying it into the wild to make predictions, and then using that deployed model to collect examples of edge cases to repeat and improve.

Licensing

Ultralytics offers two licensing options:

The AGPL-3.0 License, an OSI-approved open-source license ideal for students and enthusiasts.
The Enterprise License for businesses seeking to incorporate our AI models into their products and services.
For more details see Ultralytics Licensing.

YOLOv5 models must be trained on labelled data in order to learn classes of objects in that data. There are two options for creating your dataset before you start training:

Option 1: Create a Roboflow Dataset
1.1 Collect Images
Your model will learn by example. Training on images similar to the ones it will see in the wild is of the utmost importance. Ideally, you will collect a wide variety of images from the same configuration (camera, angle, lighting, etc.) as you will ultimately deploy your project.

If this is not possible, you can start from a public dataset to train your initial model and then sample images from the wild during inference to improve your dataset and model iteratively.

1.2 Create Labels
Once you have collected images, you will need to annotate the objects of interest to create a ground truth for your model to learn from.

YOLOv5 accuracies

Roboflow Annotate is a simple web-based tool for managing and labeling your images with your team and exporting them in YOLOv5's annotation format.

1.3 Prepare Dataset for YOLOv5
Whether you label your images with Roboflow or not, you can use it to convert your dataset into YOLO format, create a YOLOv5 YAML configuration file, and host it for importing into your training script.

Create a free Roboflow account and upload your dataset to a Public workspace, label any unannotated images, then generate and export a version of your dataset in YOLOv5 Pytorch format.

Note: YOLOv5 does online augmentation during training, so we do not recommend applying any augmentation steps in Roboflow for training with YOLOv5. But we recommend applying the following preprocessing steps:

Recommended Preprocessing Steps

Auto-Orient - to strip EXIF orientation from your images.
Resize (Stretch) - to the square input size of your model (640x640 is the YOLOv5 default).
Generating a version will give you a snapshot of your dataset, so you can always go back and compare your future model training runs against it, even if you add more images or change its configuration later.

Export in YOLOv5 Format

Export in YOLOv5 Pytorch format, then copy the snippet into your training script or notebook to download your dataset.

Roboflow dataset download snippet

Option 2: Create a Manual Dataset
2.1 Create dataset.yaml
COCO128 is an example small tutorial dataset composed of the first 128 images in COCO train2017. These same 128 images are used for both training and validation to verify our training pipeline is capable of overfitting. data/coco128.yaml, shown below, is the dataset config file that defines 1) the dataset root directory path and relative paths to train / val / test image directories (or *.txt files with image paths) and 2) a class names dictionary:


# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
path: ../datasets/coco128  # dataset root dir
train: images/train2017  # train images (relative to 'path') 128 images
val: images/train2017  # val images (relative to 'path') 128 images
test:  # test images (optional)

# Classes (80 COCO classes)
names:
  0: person
  1: bicycle
  2: car
  # ...
  77: teddy bear
  78: hair drier
  79: toothbrush
2.2 Create Labels
After using an annotation tool to label your images, export your labels to YOLO format, with one *.txt file per image (if no objects in image, no *.txt file is required). The *.txt file specifications are:

One row per object
Each row is class x_center y_center width height format.
Box coordinates must be in normalized xywh format (from 0 to 1). If your boxes are in pixels, divide x_center and width by image width, and y_center and height by image height.
Class numbers are zero-indexed (start from 0).
Roboflow annotations

The label file corresponding to the above image contains 2 persons (class 0) and a tie (class 27):

Roboflow dataset preprocessing

2.3 Organize Directories
Organize your train and val images and labels according to the example below. YOLOv5 assumes /coco128 is inside a /datasets directory next to the /yolov5 directory. YOLOv5 locates labels automatically for each image by replacing the last instance of /images/ in each image path with /labels/. For example:


../datasets/coco128/images/im0.jpg  # image
../datasets/coco128/labels/im0.txt  # label
YOLOv5 dataset structure

3. Select a Model
Select a pretrained model to start training from. Here we select YOLOv5s, the second-smallest and fastest model available. See our README table for a full comparison of all models.

YOLOv5 models

4. Train
Train a YOLOv5s model on COCO128 by specifying dataset, batch-size, image size and either pretrained --weights yolov5s.pt (recommended), or randomly initialized --weights '' --cfg yolov5s.yaml (not recommended). Pretrained weights are auto-downloaded from the latest YOLOv5 release.


python train.py --img 640 --epochs 3 --data coco128.yaml --weights yolov5s.pt
Tip

💡 Add --cache ram or --cache disk to speed up training (requires significant RAM/disk resources).

Tip

💡 Always train from a local dataset. Mounted or network drives like Google Drive will be very slow.

All training results are saved to runs/train/ with incrementing run directories, i.e. runs/train/exp2, runs/train/exp3 etc. For more details see the Training section of our tutorial notebook. Open In Colab Open In Kaggle

5. Visualize
Comet Logging and Visualization 🌟 NEW
Comet is now fully integrated with YOLOv5. Track and visualize model metrics in real time, save your hyperparameters, datasets, and model checkpoints, and visualize your model predictions with Comet Custom Panels! Comet makes sure you never lose track of your work and makes it easy to share results and collaborate across teams of all sizes!

Getting started is easy:


pip install comet_ml  # 1. install
export COMET_API_KEY=<Your API Key>  # 2. paste API key
python train.py --img 640 --epochs 3 --data coco128.yaml --weights yolov5s.pt  # 3. train
To learn more about all the supported Comet features for this integration, check out the Comet Tutorial. If you'd like to learn more about Comet, head over to our documentation. Get started by trying out the Comet Colab Notebook: Open In Colab
