import numpy as np
import cv2
import os
from retinaface import RetinaFace
from mtcnn import MTCNN

def detect_face(img_path,det):
    detected=False
    image = cv2.imread(img_path)
    if det== "RetinaFace":
        obj = RetinaFace.detect_faces(img_path)
        print(len(obj))
        if (len(obj) > 1):
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
    image = cv2.imread(img_path)
    directory = (r'C:\Users\HP\PycharmProjects\pythonProject\step1\degradedImages')
    os.chdir(directory)
    filename = "detected.jpg"
    detected= detect_face(img_path,"RetinaFace")
    cv2.imwrite(filename, detected)
