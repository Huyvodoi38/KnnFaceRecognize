import sqlite3

# Tạo kết nối đến cơ sở dữ liệu (nếu chưa có sẽ tự động tạo mới)
conn = sqlite3.connect('Nhanvien.db')

# Tạo con trỏ để thực thi các câu lệnh SQL
cursor = conn.cursor()

# Tạo bảng với 3 cột: id (số nguyên chính), name (text), numberCheck (số nguyên)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        numberCheck INTEGER DEFAULT 0
    )
''')

# Lưu các thay đổi vào cơ sở dữ liệu
conn.commit()

# Đóng kết nối
conn.close()