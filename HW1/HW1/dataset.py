import os
import cv2
import glob
import pathlib
import numpy as np


def load_data_small():
    """
        This function loads images form the path: 'data/data_small' and return the training
        and testing dataset. The dataset is a list of tuples where the first element is the 
        numpy array of shape (m, n) representing the image the second element is its 
        classification (1 or 0).

        Parameters:
            None

        Returns:
            dataset: The first and second element represents the training and testing dataset respectively
    """

    # Begin your code (Part 1-1)
    """
    First, read the images from the path: 'data/data_small'. Second, convert the images to grayscale.
    Then, mark the images as face, using 1, or non-face, using 0, and store them in the dataset.
    Finally, split the dataset into training and testing dataset.
    """
    curr_path = pathlib.Path(__file__).parent.resolve()
    train_data_path = os.path.join(curr_path, "data/data_small/train")
    train_data_path = os.path.normpath(train_data_path)
    train_data_set = []
    for file in os.listdir(os.path.join(train_data_path, "face")):
        img = cv2.imread(os.path.join(train_data_path, "face", file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (19, 19))
        train_data_set.append((img, 1))
    for file in os.listdir(os.path.join(train_data_path, "non-face")):
        img = cv2.imread(os.path.join(train_data_path, "non-face", file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (19, 19))
        train_data_set.append((img, 0))
    test_data_path = os.path.join(curr_path, "data/data_small/test")
    test_data_path = os.path.normpath(test_data_path)
    test_data_set = []
    for file in os.listdir(os.path.join(test_data_path, "face")):
        if file.endswith(".pgm"):
            img = cv2.imread(os.path.join(test_data_path, "face", file))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (19, 19))
            test_data_set.append((img, 1))
    for file in os.listdir(os.path.join(test_data_path, "non-face")):
        if file.endswith(".pgm"):
            img = cv2.imread(os.path.join(test_data_path, "non-face", file))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (19, 19))
            test_data_set.append((img, 0))
    dataset = (train_data_set, test_data_set)
    # print(dataset)
    # End your code (Part 1-1)
    
    return dataset


def load_data_FDDB(data_idx="01"):
    """
        This function generates the training and testing dataset  form the path: 'data/data_small'.
        The dataset is a list of tuples where the first element is the numpy array of shape (m, n)
        representing the image the second element is its classification (1 or 0).
        
        In the following, there are 4 main steps:
        1. Read the .txt file
        2. Crop the faces using the ground truth label in the .txt file
        3. Random crop the non-faces region
        4. Split the dataset into training dataset and testing dataset
        
        Parameters:
            data_idx: the data index string of the .txt file

        Returns:
            train_dataset: the training dataset
            test_dataset: the testing dataset
    """
    curr_path = pathlib.Path(__file__).parent.resolve()
    file_path = os.path.join(curr_path, "data/data_FDDB/FDDB-folds/FDDB-fold-{}-ellipseList.txt".format(data_idx))
    file_path = os.path.normpath(file_path)
    with open(file_path) as file:
        line_list = [line.rstrip() for line in file]

    # Set random seed for reproducing same image croping results
    np.random.seed(0)

    face_dataset, nonface_dataset = [], []
    line_idx = 0

    # Iterate through the .txt file
    # The detail .txt file structure can be seen in the README at https://vis-www.cs.umass.edu/fddb/
    while line_idx < len(line_list):
        file_path = os.path.join(curr_path, 'data/data_FDDB/originalPics', line_list[line_idx] + '.jpg')
        file_path = os.path.normpath(file_path)
        img_gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        num_faces = int(line_list[line_idx + 1])

        # Crop face region using the ground truth label
        face_box_list = []
        for i in range(num_faces):
            # Here, each face is denoted by:
            # <major_axis_radius minor_axis_radius angle center_x center_y 1>.
            coord = [int(float(j)) for j in line_list[line_idx + 2 + i].split()]
            x, y = coord[3] - coord[1], coord[4] - coord[0]            
            w, h = 2 * coord[1], 2 * coord[0]

            left_top = (max(x, 0), max(y, 0))
            right_bottom = (min(x + w, img_gray.shape[1]), min(y + h, img_gray.shape[0]))
            face_box_list.append([left_top, right_bottom])
            # cv2.rectangle(img_gray, left_top, right_bottom, (0, 255, 0), 2)

            img_crop = img_gray[left_top[1]:right_bottom[1], left_top[0]:right_bottom[0]].copy()
            face_dataset.append((cv2.resize(img_crop, (19, 19)), 1))

        line_idx += num_faces + 2

        # Random crop N non-face region
        # Here we set N equal to the number of faces to generate a balanced dataset
        # Note that we have alreadly save the bounding box of faces into `face_box_list`, you can utilize it for non-face region cropping
        for i in range(num_faces):
            # Begin your code (Part 1-2)
            """
            First, get the size of the image. Second, randomly crop the non-face region.
            Then, determine whether the non-face region is overlap with the face region.
            If not, crop and store the non-face region in the dataset. If yes, skip this 
            non-face region.
            """
            h, w = img_gray.shape
            left_top = (np.random.randint(0, w - 19), np.random.randint(0, h - 19))
            exist_face = False
            for face_box in face_box_list:
                if left_top[0] > face_box[0][0] and left_top[1] > face_box[0][1] and left_top[0] < face_box[1][0] and left_top[1] < face_box[1][1]:
                    exist_face = True
                    break 
            if not exist_face:
                img_crop = img_gray[left_top[1]:left_top[1] + 19, left_top[0]:left_top[0] + 19].copy()
            else:
                i -= 1
                continue
            # End your code (Part 1-2)

            nonface_dataset.append((cv2.resize(img_crop, (19, 19)), 0))

        # cv2.imshow("windows", img_gray)
        # cv2.waitKey(0)

    # train test split
    num_face_data, num_nonface_data = len(face_dataset), len(nonface_dataset)
    SPLIT_RATIO = 0.7

    train_dataset = face_dataset[:int(SPLIT_RATIO * num_face_data)] + nonface_dataset[:int(SPLIT_RATIO * num_nonface_data)]
    test_dataset = face_dataset[int(SPLIT_RATIO * num_face_data):] + nonface_dataset[int(SPLIT_RATIO * num_nonface_data):]

    return train_dataset, test_dataset


def create_dataset(data_type):
    if data_type == "small":
        return load_data_small()
    else:
        return load_data_FDDB()
