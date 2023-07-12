import numpy as np
import cv2
import os
import pandas as pd
from retinaface import RetinaFace
from mtcnn import MTCNN
import PIL
from PIL import Image
import torch
import lpips
from torchvision.transforms import ToTensor
from matplotlib.figure import Figure
from sklearn.preprocessing import MinMaxScaler

def get_name_num_from_img(image_path):
    # Split the image path using "/"
    path_parts = image_path.split("\\")

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
    return best_threshold, acc, far, frr,train


def detect_face(img_path,det):
    detected=False
    image = cv2.imread(img_path)
    print(img_path)
    if det== "RetinaFace":
        obj = RetinaFace.detect_faces(img_path)
        print(f"len = {len(obj)}")
        print(type(obj))
        if (len(obj) > 0 and isinstance(obj, dict)):
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
# functions to calculate metrics in the image restoration page
def crop_img(path, aligned=False):
    image = cv2.imread(path)
    # Initialize MTCNN
    detector = MTCNN()
    top_margin = 80
    bottom_margin = 15
    left_margin = 70
    right_margin = 70
    # Detect faces
    faces = detector.detect_faces(image)
    # Calculate the area of each face and store the area with the index in a list
    areas = [(i, w * h) for i, face in enumerate(faces) for _, _, w, h in [face['box']]]

    # Sort the areas list in descending order based on area
    areas.sort(key=lambda x: x[1], reverse=True)

    # Print the first element in the sorted areas list
    if (len(areas) > 0):
        first_area = areas[0]
        face_index = first_area[0]
        main_face = faces[face_index]
        x, y, w, h = main_face['box']
        # Calculate the adjusted ROI coordinates
        adjusted_x = max(x - left_margin, 0)
        adjusted_y = max(y - top_margin, 0)
        adjusted_width = w + left_margin + right_margin
        adjusted_height = h + top_margin + bottom_margin

        # Ensure the adjusted ROI coordinates are within the image boundaries
        adjusted_x = min(adjusted_x, image.shape[1] - adjusted_width)
        adjusted_y = min(adjusted_y, image.shape[0] - adjusted_height)
        # for alignement
        left_eye = main_face['keypoints']['left_eye']
        right_eye = main_face['keypoints']['right_eye']
        if aligned:
            print('test1')
            # Perform alignment based on eye positions
            dx = right_eye[0] - left_eye[0]
            dy = right_eye[1] - left_eye[1]
            angle = -np.degrees(np.arctan2(dy, dx))

            # Rotate the cropped image
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
            aligned_face = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC)
        # Crop the image using the adjusted ROI coordinates
        cropped_image = aligned_face[adjusted_y:adjusted_y + adjusted_height, adjusted_x:adjusted_x + adjusted_width]
    else:
        if (len(faces) > 0):
            main_face = faces[0]
            x, y, w, h = main_face['box']
            # Calculate the adjusted ROI coordinates
            adjusted_x = max(x - left_margin, 0)
            adjusted_y = max(y - top_margin, 0)
            adjusted_width = w + left_margin + right_margin
            adjusted_height = h + top_margin + bottom_margin

            # Ensure the adjusted ROI coordinates are within the image boundaries
            adjusted_x = min(adjusted_x, image.shape[1] - adjusted_width)
            adjusted_y = min(adjusted_y, image.shape[0] - adjusted_height)
            # for alignement
            left_eye = main_face['keypoints']['left_eye']
            right_eye = main_face['keypoints']['right_eye']
            if aligned:
                print('test2')
                # Perform alignment based on eye positions
                dx = right_eye[0] - left_eye[0]
                dy = right_eye[1] - left_eye[1]
                angle = -np.degrees(np.arctan2(dy, dx))

                # Rotate the cropped image
                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
                aligned_face = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC)
            # Crop the image using the adjusted ROI coordinates
            cropped_image = aligned_face[adjusted_y:adjusted_y + adjusted_height,
                            adjusted_x:adjusted_x + adjusted_width]
        else:
            cropped_image = image

    image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)
    return (image)

def calculate_lpips_lfw(p1, p2, lpips_model):
  image1 = Image.open(p1).convert('RGB')
  image2 = Image.open(p2).convert('RGB')
  # Resize the images if necessary
  image1 = crop_img(p1, aligned=True)
  image1 = cv2.resize(image1, (112, 112))
  image2 = crop_img(p2, aligned=True)
  image2 = cv2.resize(image2, (112, 112))
  # Convert the images to tensors
  transform = ToTensor()
  image1_tensor = transform(image1).unsqueeze(0)
  image2_tensor = transform(image2).unsqueeze(0)
  dist = lpips_model.forward(image1_tensor, image2_tensor)
  dist= dist.item()
  return dist

def calculate_lpips_xqlf(p1, p2, lpips_model):
  image1 = Image.open(p1).convert('RGB')
  image2 = Image.open(p2).convert('RGB')
  # Resize the images if necessary
  image1 = crop_img(p1, aligned=True)
  image1 = cv2.resize(image1, (112,112))
  image2 = image2.resize((112, 112))

  # Convert the images to tensors
  transform = ToTensor()
  image1_tensor = transform(image1).unsqueeze(0)
  image2_tensor = transform(image2).unsqueeze(0)
  dist = lpips_model.forward(image1_tensor, image2_tensor)
  dist= dist.item()
  return dist

def calculate_ssim_crop(p1, p2):
    # Convert images to grayscale
    image1 = Image.open(p1).convert('RGB')
    image2 = Image.open(p2).convert('RGB')
    # Resize the images if necessary
    image1 = crop_img(p1, aligned=True)
    image1 = cv2.resize(image1, (512, 512))
    image2 = crop_img(p2, aligned=True)
    image2 = cv2.resize(image2, (512, 512))

    img1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Calculate SSIM using cv2.matchTemplate()
    ssim_map = cv2.matchTemplate(img1_gray, img2_gray, cv2.TM_SQDIFF_NORMED)
    ssim_score = np.mean(ssim_map)
    return ssim_score
def calculate_psnr_crop(p1, p2):
    # Calculate the MSE (Mean Squared Error)
    image1 = Image.open(p1).convert('RGB')
    image2 = Image.open(p2).convert('RGB')
    # Resize the images if necessary
    image1 = crop_img(p1, aligned=True)
    image1 = cv2.resize(image1, (512, 512))
    image2 = crop_img(p2, aligned=True)
    image2 = cv2.resize(image2, (512, 512))
    mse = np.mean((image1 - image2) ** 2)

    # Calculate the maximum possible pixel value
    max_pixel = np.max(image1)

    # Calculate the PSNR using the MSE
    psnr_score = 20 * np.log10(max_pixel / np.sqrt(mse))

    return psnr_score

def calculate_ssim(p1, p2):
    # Convert images to grayscale
    image = cv2.imread(p1)
    img1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img1 = cv2.resize(img1, (512, 512))

    image = cv2.imread(p2)
    img2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img2 = cv2.resize(img2, (512, 512))
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate SSIM using cv2.matchTemplate()
    ssim_map = cv2.matchTemplate(img1_gray, img2_gray, cv2.TM_SQDIFF_NORMED)
    ssim_score = np.mean(ssim_map)

    return ssim_score


def calculate_psnr(p1, p2):
    # Calculate the MSE (Mean Squared Error)
    image = cv2.imread(p1)
    img1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img1 = cv2.resize(img1, (512, 512))

    image = cv2.imread(p2)
    img2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img2 = cv2.resize(img2, (512, 512))
    mse = np.mean((img1 - img2) ** 2)

    # Calculate the maximum possible pixel value
    max_pixel = np.max(img1)

    # Calculate the PSNR using the MSE
    psnr_score = 20 * np.log10(max_pixel / np.sqrt(mse))

    return psnr_score
# functions used in the folds restoration page
def get_data(fold, metric):
    df=pd.read_csv('data/metrics files/iqaMetrics_file.csv')
    print (f"follld {fold}")
    if metric=='SSIM':
        col_s=4
        col_e=7
    elif metric=='PSNR':
        col_s =8
        col_e =11
    elif metric=='LPIPS':
        col_s =0
        col_e =3
    else:
        print(metric)
    if fold=='9':
        row_s = (int(fold)) * 1323
        sub_df = df.iloc[row_s:, col_s: col_e+1]
    elif fold=='ALL':
        sub_df=df.iloc[:, col_s:col_e+1]
    else:
        row_s = (int(fold)) * 1323
        row_e = row_s + 1323
        sub_df = df.iloc[row_s:row_e,col_s:col_e+1]

    print(sub_df.shape,sub_df.columns)
    return sub_df

def calculate_column_means(df, metric_type):
    means = df.mean().tolist()
    if metric_type == 'LPIPS':
        min_index = means.index(min(means))
        max_index= means.index(max(means))
        #return means, min_index,max_index
    else :
        max_index = means.index(max(means))
        min_index=means.index(min(means))
    return means, max_index,min_index


import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def normalize_column(column):
    # Create a MinMaxScaler object
    scaler = MinMaxScaler(feature_range=(-1, 1))

    # Reshape the column to a 2-dimensional array
    reshaped_column = column.values.reshape(-1, 1)

    # Fit and transform the column using the scaler
    normalized_column = scaler.fit_transform(reshaped_column)

    # Create a DataFrame with the normalized column
    normalized_df = pd.DataFrame(normalized_column, columns=[column.name])

    return normalized_df


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




