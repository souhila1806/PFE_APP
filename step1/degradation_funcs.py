import numpy as np
import cv2
import os

# noise


def generate_noise(image,mean,var):
    # rows, cols, channels= image.shape
    noise = np.zeros(image.shape, np.uint8)
    cv2.randn(noise, mean, var)
    # noise = np.random.normal(int(mean), int(var), (rows, cols, channels)).astype('uint8')
    img_noise = cv2.add(image, noise)
    return img_noise


if __name__ == '__main__':
    image = cv2.imread("randomCompleteLQImages\Laura_Bush_0007.jpg")
    directory = (r'C:\Users\HP\PycharmProjects\pythonProject\step1\degradedImages')
    os.chdir(directory)
    filename = "degraded.jpg"
    noisy = generate_noise(image,0,100)
    cv2.imwrite(filename, noisy)
