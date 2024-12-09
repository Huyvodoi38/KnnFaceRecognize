import cv2
import sqlite3
import os

cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Hàm cập nhật tên và ID vào CSDL
def insertOrUpdate(id, name):
    conn = sqlite3.connect("Nhanvien.db")
    cursor = conn.execute('SELECT * FROM people WHERE id=' + str(id))
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
        break

    if isRecordExist == 1:
        cmd = "UPDATE people SET name=' " + str(name) + " ' WHERE id=" + str(id)
    else:
        cmd = "INSERT INTO people(id,name) Values(" + str(id) + ",' " + str(name) + " ' )"

    conn.execute(cmd)
    conn.commit()
    conn.close()


id = input('Nhập mã nhân viên:')
name = input('Nhập tên nhân viên:')
print("Nhấn f để bắt đầu chụp ảnh nhân viên, nhấn esc để thoát!")

insertOrUpdate(id, name)

sampleNum = 0

takeImg = False

path = os.path.join("dataSet", id)
os.makedirs(path, exist_ok=True)

while (True):

    ret, img = cam.read()
    ret2, image = cam.read()

    # Lật ảnh cho đỡ bị ngược
    img = cv2.flip(img, 1)
    image = cv2.flip(img, 1)

    # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
    centerH = img.shape[0] // 2
    centerW = img.shape[1] // 2
    sizeboxW = 300
    sizeboxH = 400
    cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                  (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

    # Đưa ảnh về ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Nhận diện khuôn mặt
    faces = detector.detectMultiScale(gray, 1.2, 5)
    for (x, y, w, h) in faces:
        # Vẽ hình chữ nhật quanh mặt nhận được
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        if takeImg == True:
            sampleNum = sampleNum + 1
            # Ghi dữ liệu khuôn mặt vào thư mục dataSet
            img_path = os.path.join(path, "img_{}.jpg".format(sampleNum))
            cv2.imwrite(img_path, image)

    # Nhấn F để bắt đầu lưu ảnh
    if cv2.waitKey(1) & 0xFF == ord('f'):
        print("Da nhan nut f")
        takeImg = True

    cv2.imshow('frame', img)

    # Check xem có bấm esc hoặc trên 100 ảnh sample thì thoát
    if cv2.waitKey(1) & 0xFF == 27:
        break
    elif sampleNum > 49:
        break

cam.release()
cv2.destroyAllWindows()
