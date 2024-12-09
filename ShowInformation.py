import sqlite3
from tkinter import Tk, ttk

def show_employee_table():
    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect('Nhanvien.db')
    cursor = conn.cursor()

    # Lấy dữ liệu từ bảng (giả sử bảng có tên là 'people')
    query = "SELECT * FROM people"
    cursor.execute(query)
    data = cursor.fetchall()

    # Tạo cửa sổ Tkinter
    root = Tk()
    root.title("Danh sách nhân viên")

    # Tạo bảng Treeview để hiển thị dữ liệu
    tree = ttk.Treeview(root, columns=("id", "name","numberCheck"), show="headings")
    tree.heading("id", text="Số thứ tự")
    tree.heading("name", text="Tên nhân viên")
    tree.heading("numberCheck", text="Số lần chấm công")

    # Đưa dữ liệu vào bảng
    for row in data:
        tree.insert("", "end", values=row)

    tree.pack(expand=True, fill="both")

    # Chạy vòng lặp giao diện
    root.mainloop()

    # Đóng kết nối cơ sở dữ liệu
    conn.close()

# Gọi hàm hiển thị
show_employee_table()
