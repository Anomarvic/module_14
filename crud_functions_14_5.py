import sqlite3

def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    ''')

    connection.commit()
    connection.close()

    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL DEFAULT 1000
    );
    ''')

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    connection.close()
    return products

def prod_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    products_data = [
        ('Продукт 1', 'Описание 1', 100),
        ('Продукт 2', 'Описание 2', 200),
        ('Продукт 3', 'Описание 3', 300),
        ('Продукт 4', 'Описание 4', 400)
    ]

    # Чтобы не комментить каждый раз
    # Проверим сколько в базе есть продуктов
    # Добавляем продукты только если их количество не равно задуманному
    cursor.execute('SELECT * FROM Products')
    product_list_length = len(cursor.fetchall())

    if product_list_length != len(products_data):
        for i in range(len(products_data)):
            cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', (products_data[i][0], products_data[i][1], products_data[i][2]))

    connection.commit()
    connection.close()

if __name__ == '__main__':
    prod_db()


def add_user(username, email, age):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age) VALUES(?, ?, ?)', (username, email, age))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    user = cursor.fetchone()

    connection.close()
    return user is not None

def us_db():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    users_data = [
        ('newuser', 'user1@gmail.com', 25),
        ('newuserr', 'user2@gmail.com', 33),
        ('nnewuser', 'user3@gmail.com', 45),
        ('newuuser', 'user4@gmail.com', 28)
    ]

    # Чтобы не комментить каждый раз
    # Проверим сколько в базе есть users
    # Добавляем users только если их количество не равно задуманному
    cursor.execute('SELECT * FROM Users')
    users_list_length = len(cursor.fetchall())

    if users_list_length != len(users_data):
        for i in range(len(users_data)):
            cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)',
                           (users_data[i][0], users_data[i][1], users_data[i][2]))

    connection.commit()
    connection.close()


if __name__ == '__main__':
    us_db()
