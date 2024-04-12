import os
from unittest import result
import cv2
import utils
import pathlib
import numpy as np
import matplotlib.pyplot as plt


def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:A
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    """
    First, read the images according to the path in the detectData.txt file.
    Second, convert the images to grayscale. Next, determine the face area 
    using the label in the detectData.txt file. Then, use the clf.classify()
    function to detect the face and draw the box on the image. If the result is
    true, draw the green box on the image. Otherwise, draw the red box on the image.
    Finally, show the face detection results and save the result image.
    """
    curr_path = pathlib.Path(__file__).parent.absolute()
    dataPath = os.path.join(curr_path, dataPath)
    dataPath = os.path.normpath(dataPath)
    with open(dataPath, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if line.split()[0].endswith('.jpg'):
              img_name = line.split()[0]
              img_path = os.path.join(curr_path, 'data/detect', img_name)
              img = cv2.imread(img_path)
              img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
              if img is None:
                print(f'Image {img_path} not found')
                continue
              img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
              items = int(line.split()[1])
              for j in range(items):
                x, y, w, h = lines[i + j + 1].split()[0:4]
                x, y, w, h = int(x), int(y), int(w), int(h)
                face = img_gray[y : y + h, x : x + w]
                face = cv2.resize(face, (19, 19))
                result = clf.classify(face)
                if result:
                  cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                  cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
              i += items
              plt.imshow(img)
              plt.show()
              save_path = os.path.join(curr_path, 'data/detect/result_{}.jpg'.format(img_name.split('.')[0]))
              save_path = os.path.normpath(save_path)
              if os.path.exists(save_path):
                  os.remove(save_path)
              if cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_BGR2RGB), [int(cv2.IMWRITE_JPEG_QUALITY), 90]):
                print('Result saved')
    # End your code (Part 4)
