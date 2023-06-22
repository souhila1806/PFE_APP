import numpy as np
import cv2
import os

# noise


def generate_noise(image):
    # rows, cols, channels= image.shape
    mean = 0
    var = 180
    noise = np.zeros(image.shape, np.uint8)
    cv2.randn(noise, mean, var)
    # noise = np.random.normal(int(mean), int(var), (rows, cols, channels)).astype('uint8')
    img_noise = cv2.add(image, noise)
    return img_noise


if __name__ == '__main__':
    image = cv2.imread("randomCompleteLQImages\Jeffrey_Archer_0001.jpg")
    directory = (r'C:\Users\HP\PycharmProjects\pythonProject\step1\degradedImages')
    os.chdir(directory)
    filename = "Jeffrey_Archer_0001.jpg"
    noisy = generate_noise(image)
    cv2.imwrite(filename, noisy)