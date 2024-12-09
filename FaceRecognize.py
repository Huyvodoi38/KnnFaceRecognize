import cv2
import numpy as np
from DataPrepare import faces
from DataPrepare import labels
from DataPrepare import label_dict
import sqlite3

face_detection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Hàm lấy thông tin người dùng qua ID
def getProfile(id):
    conn=sqlite3.connect("Nhanvien.db")
    cursor=conn.execute("SELECT * FROM people WHERE id="+id)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

# Hàm cập nhật số lần chấm công
def update(k,id):
    conn = sqlite3.connect("Nhanvien.db")
    cmd = "UPDATE people SET numberCheck=" + str(k) + " WHERE id=" + id
    conn.execute(cmd)
    conn.commit()
    conn.close()

# Hàm tính khoảng cách Euclid
def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((np.array(point1) - np.array(point2)) ** 2))

# Hàm KNN với trọng số
def knn(training_data, labels, test_point, k=9):
    # Tính khoảng cách từ điểm kiểm tra đến tất cả các điểm trong tập huấn luyện
    distances = []
    for i, data_point in enumerate(training_data):
        distance = euclidean_distance(test_point, data_point)
        distances.append((distance, labels[i]))

    # Sắp xếp danh sách theo khoảng cách
    distances.sort(key=lambda x: x[0])

    # Lấy k điểm gần nhất
    nearest_neighbors = distances[:k]

    # Tính trọng số và tổng hợp điểm số cho từng nhãn
    class_weights = {}
    epsilon = 1e-6  # Tránh chia cho 0
    for distance, label in nearest_neighbors:
        weight = 1 / (distance + epsilon)
        if label in class_weights:
            class_weights[label] += weight
        else:
            class_weights[label] = weight

    # Tìm nhãn có trọng số lớn nhất
    most_common_class = max(class_weights, key=class_weights.get)

    return most_common_class

#Hàm nhận diện khuôn mặt và chấm công
def face_detect():
    cap = cv2.VideoCapture(0)
    isStart = False
    done = False
    while True:
        ret,frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            print("Camera is not working")
            break

        # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
        centerH = frame.shape[0] // 2
        centerW = frame.shape[1] // 2
        sizeboxW = 300
        sizeboxH = 400
        cv2.rectangle(frame, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

        #chuyển về ảnh đen trắng
        gray = cv2.cvtColor(frame,cv2.COLOR_RGBA2GRAY)

        #phát hiện khuôn mặt trong ảnh
        face_sv = face_detection.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5)

        #xác nhận khuôn mặt
        for (x,y,w,h) in face_sv:
            face = cv2.resize(gray[y:y+h,x:x+w],(100,100)).flatten()
            label = knn(faces, labels, face)
            profile = getProfile(label_dict[label])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(frame,profile[1],(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)
            if isStart:
                update(profile[2] + 1, label_dict[label])
                done = True
        # Hiển thị màn hình
        cv2.imshow("Face Detection",frame)
        # Thoát khi chấm công xong hoặc ấn f
        if done:
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break
        # Ấn f để bắt đầu chấm công
        if cv2.waitKey(1) & 0xFF == ord('f'):
            isStart = True
            print("start")

    cap.release()
    cv2.destroyAllWindows()

face_detect()


