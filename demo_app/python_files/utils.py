import numpy as np
import cv2
import os
import pandas as pd
from retinaface import RetinaFace
from mtcnn import MTCNN

def get_name_num_from_img(image_path):
    # Split the image path using "/"
    path_parts = image_path.split("/")

    # Get the last part of the path (name and number with extension)
    last_part = path_parts[-1]

    # Remove the file extension
    file_name = last_part.split(".")[0]

    # Split the file name into the name and number
    name, number = file_name.rsplit("_", 1)

    # Remove leading zeros from the number and convert it to an integer
    number = int(number.lstrip("0"))

    return name, number

def cross_val(data,index_val_folder):
  matched_train=pd.DataFrame()
  matched_test=pd.DataFrame()
  mismatched_train=pd.DataFrame()
  mismatched_test=pd.DataFrame()
  for i in range(10):
    matched_fold=data.iloc[i*300:(i+1)*300,:]
    mismatched_fold=data.iloc[3000+i*300:3000+(i+1)*300,:]
    if (i!=index_val_folder):
      matched_train=pd.concat([matched_train,matched_fold]).reset_index(drop=True)
      mismatched_train=pd.concat([mismatched_train,mismatched_fold]).reset_index(drop=True)
    else:
      matched_test=pd.concat([matched_test,matched_fold]).reset_index(drop=True)
      mismatched_test=pd.concat([mismatched_test,mismatched_fold]).reset_index(drop=True)
    train=pd.concat([matched_train,mismatched_train]).reset_index(drop=True)
    test = pd.concat([matched_test, mismatched_test]).reset_index(drop=True)
  return train,test

# calculate threshold acc far and frr for the ith fold of data
def calcul_threshold_acc(data,i):
    half = 2700
    ACC=[]
    train,test = cross_val(data,i)
    minimum = train.iloc[0:half, 0].min()
    maximum = train.iloc[half:, 0].max()
    threshold = minimum
    while (threshold < maximum):
        fr = train.iloc[0:half, 0][train.iloc[0:half, 0] < threshold].shape[0]
        fa = train.iloc[half:, 0][train.iloc[half:, 0] > threshold].shape[0]
        ACC.append(((half - fa) + (half - fr)) / (half * 2))
        far= fa / half
        frr= fr / half
        threshold = threshold + 0.01
    best_threshold=minimum + ACC.index(max(ACC)) * 0.01
    fr = test.iloc[0:300, 0][test.iloc[0:300, 0] < best_threshold].shape[0]
    fa = test.iloc[300:, 0][test.iloc[300:, 0] > best_threshold].shape[0]
    acc=((300 - fa) + (300 - fr)) / 600
    far=fa / 300
    frr=fr / 300
    return best_threshold, acc, far, frr


def detect_face(img_path,det):
    detected=False
    image = cv2.imread(img_path)
    if det== "RetinaFace":
        obj = RetinaFace.detect_faces(img_path)
        print(len(obj))
        if (len(obj) > 0):
            x = obj['face_1']['facial_area'][0]
            y = obj['face_1']['facial_area'][1]
            w = obj['face_1']['facial_area'][2]-x
            h = obj['face_1']['facial_area'][3]-y
            detected=True
    elif det == "MTCNN":
        detector = MTCNN()
        faces = detector.detect_faces(image)
        if len(faces) > 0:
            # Find the face with the largest area
            main_face = max(faces, key=lambda face: face['box'][2] * face['box'][3])
            x, y, w, h = main_face['box']
            detected=True
    if detected == True:
        # Draw the rectangle on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 225, 0), 2)
    return image

if __name__ == '__main__':
    img_path=r"C:\Users\HP\PycharmProjects\pythonProject\step1\randomCompleteLQImages\Laura_Bush_0007.jpg"
    #image = cv2.imread(img_path)
    #directory = (r'C:\Users\HP\PycharmProjects\pythonProject\step1\degradedImages')
    #os.chdir(directory)
    #filename = "detected.jpg"
    #detected= detect_face(img_path,"RetinaFace")
    #cv2.imwrite(filename, detected)
    name,num=get_name_num_from_img(img_path)
    print(f"name {name} and num {num}")

