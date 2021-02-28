# Copyright (c) Hiren Galiyawala, Kenil Shah, Vandit Gajjar, and Mehul S. Raval.

import os
import sys
import random
import colorsys
import cv2
import numpy as np
import matplotlib.pyplot as plt
ROOT_DIR = os.path.abspath("../")
import modalities.HeightEstimation as ht

height_pass_index =[]
# torso1_pass_index = []
# torso2_pass_index = []
IMAGE_DIR = os.path.join(ROOT_DIR, "images")
sys.path.append(ROOT_DIR)  # To find local version of the library

def torso_mask_coordinates(y1,x1,y2,x2,mask,torso_type):
    person_height = y2 - y1

    if torso_type == "Long Sleeve":
        legs = y1 + int(0.50 * person_height)
        #print("legs", legs)
        upper = y1 + int(0.22 * person_height)
        torso_length = legs - upper
    if torso_type == "Short Sleeve":
        legs = y1 + int(0.50 * person_height)
        #print("legs", legs)
        upper = y1 + int(0.22 * person_height)
        torso_length = legs - upper
    if torso_type == "No Sleeve":
        legs = y1 + int(0.50 * person_height)
        #print("legs", legs)
        upper = y1 + int(0.25 * person_height)
        torso_length = legs - upper
    if torso_type == "dress":
        legs = y1 + int(0.56 * person_height)
        #print("legs", legs)
        upper = y1 + int(0.19 * person_height)
        torso_length = legs - upper

    try:
        m = -1

        while (mask[upper][x1 + m]) == False:
            m = m + 1
        segment_up_x = x1 + m

        # print(segment_up_x)
        m = -1
        # print("1")
        while (mask[legs][x1 + m]) == False:
            m = m + 1
        segment_legs_x = x1 + m

        segment_x = max(segment_legs_x, segment_up_x)
        m = -1
        # print("2")
        while (mask[upper][x2 + m]) == False:
            m = m - 1
        segment_up2_x = x2 + m
        m = -1
        # print("3")
        while (mask[legs][x2 + m]) == False:
            m = m - 1
        segment_legs2_x = x2+m
        # print("4")
        segment_x2 = min(segment_legs2_x, segment_up2_x)
        a=[upper, legs, segment_x, segment_x2, torso_length]
    except:
        a=[-1]
    return a


def height_estimation(x1,y1,x2,y2,mask,camera):
    actual_height = ht.main(x1,y1,x2,y2,mask,camera)
    actual_height = int(actual_height)
    return actual_height


'''
If the height of person does not fall into the input category, that particular person is filtered here.
INPUT:
    actual_height: Height which is determined buy the algorithm
    min_height:The minimum height of the person as given in the input query
    max_height: The maximum height of the person as given in the input query 
'''
def height_filter(actual_height, min_height, max_height, i):
    flag = 0
    if actual_height < (min_height - 10):
        flag = 1
    if actual_height > (max_height + 10):
        flag = 1
    height_pass_index.append(i)
    return height_pass_index, flag


'''
The torso color of the person is classified in the color_classification function.
INPUT:
    image: Input image fetched form the video frame
    x1,y1,x2,y2: bounding box of person
    masks: Semantic Segmentation obtained from the Mask-RCNN for that particular person
    torso_type: Type of the torso which person is wearing
    ColorModel: Densenet Color Model
'''
def color_classification(image, x1,y1,x2,y2, masks, torso_type, ColorModel):
    coord = torso_mask_coordinates(y1,x1,y2,x2,masks,torso_type)

    upper = coord[0]
    legs = coord[1]
    segment_x = coord[2]
    segment_x2 = coord[3]
    img2 = image[upper:legs, segment_x:segment_x2]

    cv2.imwrite("modalities/torso_color/images/1.png", img2)
    # cv2.imwrite("modalities/torso_color/images/"+image_name+str(patchFlag)+"torso.jpg",img2)
    # print("Entered in Torso")
    for file_name in sorted(os.listdir("modalities/torso_color/images/")):
        try:
            img_a = cv2.imread("modalities/torso_color/images/" + file_name)
            # img_a = cv2.imread("modalities/torso_color/images/"+image_name+str(patchFlag)+"torso.jpg")
            # img_a = img2
            img_a = cv2.resize(img_a.astype(np.float32), (224, 224))
            img_a = np.expand_dims(img_a, axis=0)
            # img_a = img_a.reshape((1,227,227,3))
        except:
            print("null img error")
            continue
        out = ColorModel.predict(img_a)
        sorted_predict = np.argsort(out)
        classes = []
        with open('modalities/torso_color/ColorClasses.txt', 'r') as list_:
            for line in list_:
                classes.append(line.rstrip('\n'))
        class_name1 = str(classes[sorted_predict[0][11]])
        class_name2 = str(classes[sorted_predict[0][10]])
        print("class_name1:", class_name1, ", class_name2:", class_name2)
        return class_name1, class_name2


'''
Person are filtered using detected colors and torso color provided by user.
INPUT:
    i
    color_class1: Color1 determined from the color_classification function
    color_class2: Color1 determined from the color_classification function
    torso_color: Original color query of the person
'''

def color_filter(i, color_class1, color_class2, torso_color):
    # print("i",i)
    array_name = None
    if color_class1 == torso_color:
        #torso1_pass_index.append(i)
        array_name = "torso1_pass_index"
        print("Color Detected")

    if color_class2 == torso_color:
        #torso2_pass_index.append(i)
        print("Color Detected")
        array_name = "torso2_pass_index"

    #print(torso1_pass_index, "Torso 1")
    #print(torso2_pass_index, "Torso 2")

    return array_name



'''
Persons gender is classified using the the gender_classification function.
INPUT:
    x1,y1,x2,y2 = Bounding box of person
    img = Input frame(Fetched from Input Video)
    GenderModel = Dense-net Model for Gender Classification 
'''

def gender_classification(x1,y1,x2,y2,img,GenderModel):
    gender_image = img[y1:y2, x1:x2]
    cv2.imwrite("modalities/gender/images/1.png", gender_image)

    for file_name in sorted(os.listdir("modalities/gender/images/")):
        img_a = cv2.imread("modalities/gender/images/1.png")
        img_a = cv2.resize(img_a.astype(np.float32), (140, 350))
        img_a = np.expand_dims(img_a, axis=0)
        out = GenderModel.predict(img_a)
        classes = []
        with open('modalities/gender/GenderClasses.txt', 'r') as list_:
            for line in list_:
                classes.append(line.rstrip('\n'))
        gender_name = str(classes[np.argmax(out)])
        break
    return gender_name


'''
Function = person_identification
It identifies the person based on query given by user. 
The function stores the surveillance frame with bounding box around the identified person.
INPUT:
    rois = Bounding box of person
    frame = Input frame(Fetched from Input Video)
    GenderModel = Dense-net Model for Gender Classification
    ColorModel = Dense-net Model for Color Classification
    frame_name = Name of the frame
    masks = Semantic Segmentation obtained from the Mask-RCNN
    output_storage_path = The path where the text file and images are stored 
    attributes = Person Queries
'''

def person_identification(frame_name, frame, rois, masks, class_ids, scores, class_names, color_model=None, gender_model = None, text_file=None, output_storage_path=None, attributes=None):

    height_pass_index = []
    torso1_pass_index = []
    torso2_pass_index = []
    person_id = 1
    camera_calibration, min_height, max_height, torso_color, torso_type, gender_type = attributes
    camera = 2
    boxes = rois
    N = rois.shape[0]
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontColor = (0, 0, 255)
    lineType = 2
    #print("In beginning torso1_pass_index,torso2_pass_index",torso1_pass_index,torso2_pass_index)
    if not N:
        print("\n*** No instances to display *** \n")
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]
    img = frame
    print("camera_calibaration:",camera_calibration)
    # print("torso1_pass_index ")
    if camera_calibration == "1":
        # height_pass_index = []
        # torso1_pass_index = []
        # torso2_pass_index = []
        print("frame_name",frame_name)
        for i in range(N):
            mask = masks[:, :, i]
            if not (np.any(boxes[i])):
                continue
            if class_ids[i] != 1:
                continue
            if scores[i] < 0.8:
                continue
            y1, x1, y2, x2 = boxes[i]
            actual_height = height_estimation(x1, y1, x2, y2, mask,camera)
            person_index, flag = height_filter(actual_height, max_height, min_height,i)
            if flag == 1:
                continue
            try:
                color_class1, color_class2 = color_classification(img, x1,y1,x2,y2, mask, torso_type, color_model)
            except:
                continue
            array_name = color_filter(i, color_class1, color_class2, torso_color)
            if array_name == "torso1_pass_index":
                torso1_pass_index.append(i)
            if array_name == "torso2_pass_index":
                torso2_pass_index.append(i)

        final_torso = torso1_pass_index
        if len(torso1_pass_index) == 1:
            print("Determined using Torso Color 1")
            y1, x1, y2, x2 = boxes[torso1_pass_index[0]]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, str(person_id), (x1, y1 + 25), font, 1, (0, 0, 255), 2, lineType)
            text_file.write(str(frame_name)+","+str(person_id)+ "," + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2)+"\n")
            person_id = person_id + 1

        if len(torso1_pass_index) == 0:
            final_torso = torso2_pass_index
            if len(torso2_pass_index) == 1:
                print("Determined using Torso Color 2")
                y1, x1, y2, x2 = boxes[torso2_pass_index[0]]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, str(person_id), (x1, y1 + 25), font, 1, (0, 0, 255), 2, lineType)
                text_file.write(str(frame_name) + "," + str(person_id) + "," + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2) + "\n")
                person_id = person_id + 1

            if len(torso2_pass_index) == 0:

                N = boxes.shape[0]
                print("Number of boxes=", N)
                for i in range(N):
                    mask = masks[:, :, i]
                    if not (np.any(boxes[i])):
                        continue
                    if class_ids[i] != 1:
                        continue
                    if scores[i] < 0.8:
                        continue
                    y1, x1, y2, x2 = boxes[i]
                    try:
                        color_class1, color_class2 = color_classification(img, x1, y1, x2, y2, mask, torso_type, color_model)
                    except:
                        continue
                    array_name = color_filter(i, color_class1, color_class2, torso_color)
                    if array_name == "torso1_pass_index":
                        torso1_pass_index.append(i)
                    if array_name == "torso2_pass_index":
                        torso2_pass_index.append(i)
                final_torso = torso1_pass_index
                if len(torso1_pass_index) == 1:
                    print("Determined using Torso Color 1")
                    y1, x1, y2, x2 = boxes[torso1_pass_index[0]]
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img,str(person_id),(x1,y1 + 25),font,1,(0,0,255),2,lineType)
                    text_file.write(str(frame_name) + "," +str(person_id)+ "," + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2) + "\n")
                    person_id = person_id + 1

                if len(torso1_pass_index) == 0:
                    final_torso = torso2_pass_index
                    if len(torso2_pass_index) == 1:
                        print("Determined using Torso Color 2")
                        y1, x1, y2, x2 = boxes[torso2_pass_index[0]]
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img, str(person_id), (x1, y1 + 25), font, 1, (0, 0, 255), 2, lineType)
                        text_file.write(str(frame_name)+"," +str(person_id)+ "," + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2) + "\n")
                        person_id = person_id + 1


    else:
        # print("N =", N)

        # height_pass_index = []
        # torso1_pass_index = []
        # torso2_pass_index = []
        print("frame_name:", frame_name)
        for i in range(N):
            # print("i",i)
            mask = masks[:, :, i]
            if not (np.any(boxes[i])):
                continue
            if class_ids[i] != 1:
                continue
            if scores[i] < 0.8:
                continue
            y1, x1, y2, x2 = boxes[i]
            # print("y1,x1,y2,x2",y1,x1,y2,x2)
            try:
                color_class1, color_class2 = color_classification(img, x1, y1, x2, y2, mask, torso_type, color_model)
                array_name = color_filter(i, color_class1, color_class2, torso_color)
            except:
                continue
            if array_name == "torso1_pass_index":
                torso1_pass_index.append(i)
            if array_name == "torso2_pass_index":
                torso2_pass_index.append(i)
            # print("torso_1_pass_index , torso_2_pass_index",torso1_pass_index,torso2_pass_index)

        final_torso = torso1_pass_index
        if len(torso1_pass_index) == 1:
            print("Determined using Torso Color 1")
            y1, x1, y2, x2 = boxes[torso1_pass_index[0]]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, str(person_id), (x1, y1 + 25), font, 1, (0, 0, 255), 2, lineType)
            text_file.write(str(frame_name) +","+str(person_id)+ "," + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2)+"\n")
            person_id = person_id + 1

        if len(torso1_pass_index) == 0:
            final_torso = torso2_pass_index
            if len(torso2_pass_index) == 1:
                print("Determined using Torso Color 2")
                y1, x1, y2, x2 = boxes[torso2_pass_index[0]]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, str(person_id), (x1, y1 + 25), font, 1, (0, 0, 255), 2, lineType)
                text_file.write(str(frame_name)+","+str(person_id)+ "," + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2) + "\n")
                person_id = person_id + 1

    if len(final_torso) > 1:
        i = 0
        print("final_torso:",final_torso)
        while i < len(final_torso):
            print("Gender Channel")
            if not (np.any(boxes[final_torso[i]])):
                continue
            if class_ids[final_torso[i]] != 1:
                continue
            y1, x1, y2, x2 = boxes[final_torso[i]]
            gender_name = gender_classification(x1, y1, x2, y2, img, gender_model)
            if gender_type == gender_name:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, str(person_id), (x1, y1 + 25), font, 1, (0, 0, 255), 2, lineType)
                text_file.write(str(frame_name)+","+str(person_id)+ "," + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2)+"\n")
                person_id = person_id + 1
            i = i+1

#    cv2.imshow("",img)
    cv2.imwrite(output_storage_path+str(frame_name)+".jpg", img)

