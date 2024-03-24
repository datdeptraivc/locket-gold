import asyncio
import websockets
import pyodbc
from datetime import datetime
import urllib.parse

def connect_to_database():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password')

def create_user_information_table():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'user_information')
        BEGIN
            CREATE TABLE user_information (
                id_user INT PRIMARY KEY IDENTITY,
                username NVARCHAR(50) NOT NULL,
                password NVARCHAR(50) NOT NULL,
                email NVARCHAR(50) NOT NULL,
                realname NVARCHAR(100) NOT NULL,
                date_of_birth DATE NOT NULL
            )
        END
    ''')
    conn.commit()
    conn.close()

async def register(websocket, path):
    try:
        async for message in websocket:
            data = urllib.parse.parse_qs(message)
            if all(field in data for field in ['username', 'password', 'email', 'realname', 'dob']):
                username = data['username'][0]
                password = data['password'][0]
                email = data['email'][0]
                realname = data['realname'][0]
                dob = datetime.strptime(data['dob'][0], '%Y-%m-%d').date()
                
                conn = connect_to_database()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user_information WHERE username=?", (username,))
                existing_user = cursor.fetchone()
                if existing_user:
                    await websocket.send("Tên đăng nhập đã tồn tại!")
                else:
                    cursor.execute("INSERT INTO user_information (username, password, email, realname, date_of_birth) VALUES (?, ?, ?, ?, ?)", (username, password, email, realname, dob))
                    conn.commit()
                    conn.close()
                    await websocket.send("Đăng ký thành công!")
            else:
                await websocket.send("Dữ liệu không hợp lệ!")
    except websockets.exceptions.ConnectionClosedOK:
        print("Kết nối đã đóng.")

async def login(websocket, path):
    try:
        async for message in websocket:
            data = urllib.parse.parse_qs(message)
            if all(field in data for field in ['username', 'password']):
                username = data['username'][0]
                password = data['password'][0]
                conn = connect_to_database()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user_information WHERE username=? AND password=?", (username, password))
                user = cursor.fetchone()
                conn.close()
                if user:
                    await websocket.send("Đăng nhập thành công!")
                else:
                    await websocket.send("Đăng nhập thất bại! Vui lòng kiểm tra lại tên đăng nhập và mật khẩu.")
            else:
                await websocket.send("Dữ liệu không hợp lệ!")
    except websockets.exceptions.ConnectionClosedOK:
        print("Kết nối đã đóng.")

async def main():
    create_user_information_table()  # Tạo bảng user_information nếu chưa tồn tại
    register_server = await websockets.serve(register, "localhost", 8765)
    login_server = await websockets.serve(login, "localhost", 8766)
    await register_server.wait_closed()
    await login_server.wait_closed()

asyncio.run(main())
