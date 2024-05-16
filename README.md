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
