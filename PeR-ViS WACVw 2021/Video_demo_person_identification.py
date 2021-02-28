# Copyright (c) Hiren Galiyawala, Kenil Shah, Vandit Gajjar, and Mehul S. Raval.

import os
import cv2
import coco
import model as modellib
import PersonFilter
from DenseColor import DenseNet
from DenseGender import DenseNet as densegender
import skimage.io
from keras.optimizers import SGD
import config

# Root directory of the project
ROOT_DIR = os.getcwd()

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "mylogs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1+80

inference_config = InferenceConfig()

# Load Mask R-CNN Model (Object Detection)
model = modellib.MaskRCNN(mode="inference", config=inference_config, model_dir=MODEL_DIR)
# Get path to saved weights
model_path = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
assert model_path != "", "Provide path to trained weights"
print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)


# Load Dense-Net Model for Color Classification
ColorWeights_path = 'modalities/torso_color/color_model.h5'
ColorModel = DenseNet(reduction=0.5, classes=12, weights_path=ColorWeights_path)
sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
ColorModel.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
print("----- Color Model Loaded -----")

# Load Dense-Net Model for Gender Classification
GenderWeights_path = 'modalities/gender/gender_model.h5'
GenderModel = densegender(reduction=0.5, classes=2, weights_path=GenderWeights_path)
sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
GenderModel.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
print("----- Gender Model Loaded -----")

# Classes
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

# Attributes

input_video_path="video/video.mp4"
output_storage_path="output/"
torso_color="Blue"           # ['Black','Blue','Brown','Green','Grey','Orange','Pink','Purple','Red','White','Yellow','Skin']
torso_type = "Short Sleeve"   # ['Long Sleeve','Short Sleeve','No Sleeve']
camera_calibaration = "1"     # [0 = Camera calibration NOT available, 1 = Camera calibration available]
gender_type = "Female"        # ['Male','Female']
min_height = 150                # [130 - 160, 150 - 170, 160 - 180, 170 - 190, 180 - 210]
max_height = 170

# input_video_path = input("Video path here:\t")
# output_storage_path = input("Data storage path here:\t")
# camera_calibaration = input("Camera Calibaration(Yes-1/No-0):\t")
# if camera_calibaration == "1":
#     min_height = int(input("Minimum height:\t"))
#     max_height = int(input("Maximum height:\t"))
# else:
#     min_height = 0
#     max_height = 0
# torso_color = input("Torso_Color:\t")
# torso_type = input("Torso_Type:\t")
# gender_type = input("Gender_Type:\t")

attributes = [camera_calibaration,min_height , max_height , torso_color, torso_type, gender_type]

# Person Identification
text_file = open(output_storage_path+"/person_coordinates.txt", 'w')
text_file.write("frame_name,person_id,left,top,right,bottom\n")
text_file.close()
cap = cv2.VideoCapture(input_video_path)

frame_name = 0
while True:
    try:
        ret, frame = cap.read()
        #cv2.imwrite("InputImage.jpg",frame)
        #image = skimage.io.imread("InputImage.jpg")
        '''
        The following module detects the person in the surveillance frame. It also
        gives the semantic segmentation within the person's bounding box.
        '''
        text_file = open(output_storage_path + "/person_coordinates.txt", 'a')
        results = model.person_detection([frame], verbose=1)
        r = results[0]
        rois = r['rois']
        mask = r['masks']
        class_ids = r["class_ids"]
        scores = r["scores"]
        PersonFilter.person_identification(frame_name, frame, rois, mask, class_ids, scores, class_names, color_model=ColorModel, gender_model=GenderModel, text_file=text_file, output_storage_path=output_storage_path, attributes=attributes)
        frame_name = frame_name + 1
        text_file.close()
    except:
        break


