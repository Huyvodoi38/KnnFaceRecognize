import cv2
import os
import numpy as np

# hàm cắt lấy khuôn mặt trong ảnh và gán nhãn
def data_prepare():
    labels = []
    faces = []
    label_id = 0
    label_dict = {}
    for tensinhvien in os.listdir(dataset_path):
        anhsinhvien = os.path.join(dataset_path,tensinhvien)
        if os.path.isdir(anhsinhvien):
            label_dict[label_id] = tensinhvien
        for image_name in os.listdir(anhsinhvien):
            image_path = os.path.join(anhsinhvien,image_name)
            image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
            face_nhanvien = face_detection.detectMultiScale(image,scaleFactor=1.2,minNeighbors=5)
            for (x,y,w,h) in face_nhanvien:
                face = cv2.resize(image[y:y+h,x:x+w],(100,100))
                faces.append(face.flatten())
                labels.append(label_id)
        label_id += 1
    return np.array(faces),np.array(labels), label_dict

dataset_path = "./dataSet"
face_detection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces,labels,label_dict = data_prepare()
