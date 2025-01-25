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
