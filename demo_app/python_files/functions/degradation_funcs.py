import numpy as np
import cv2
import os
from PIL import Image

# noise


def generate_noise(image,mean,var):
    # rows, cols, channels= image.shape
    rows, cols, channels = image.shape
    noise = np.random.normal(int(mean), int(var), (rows, cols, channels)).astype('uint8')
    img_noise = cv2.add(image, noise)
    return img_noise

def generate_blur(image,kernel_size):
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blurred_image


def generate_lowresolution(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    new_image = np.full(image.shape, (128, 128, 128), dtype=np.uint8)
    x_offset = (new_image.shape[1] - resized.shape[1]) // 2
    y_offset = (new_image.shape[0] - resized.shape[0]) // 2
    new_image[y_offset:y_offset + resized.shape[0], x_offset:x_offset + resized.shape[1]] = resized
    return new_image

def generate_compression_artifact(image,quality):
    # Save the image with the specified quality
    cv2.imwrite(r"images\degradation_results\resolution.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    # Read the compressed image back using OpenCV
    image = cv2.imread(r"images\degradation_results\resolution.jpg")

    return image



if __name__ == '__main__':
    image = cv2.imread(r"data\images\XQLFW\Laura_Bush_0007.jpg")
    directory = (r'demo_app\images\degradation_results')
    os.chdir(directory)
    filename = "degraded.jpg"
    #noisy = generate_noise(image,0,100)
    blurred=generate_blur(image,101)
    #lr=generate_lowresolution(image,40)
    #comp=generate_compression_artifact(image,500)
    cv2.imwrite(filename, blurred)
