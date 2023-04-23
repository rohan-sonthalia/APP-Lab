import tkinter as tk
from tkinter import ttk
from tkinter import *

import sqlite3
from sqlite3 import Error

class Product:
    db_name = 'database.db'

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS product (Name TEXT, Price REAL)')
            conn.commit()
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
                
#     def create_table(self):
#         with sqlite3.connect(self.db_name) as conn:
#             cursor = conn.cursor()
#             cursor.execute('CREATE TABLE IF NOT EXISTS product (Name TEXT, Price REAL)')
#             conn.commit()


    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')

        frame = LabelFrame(self.wind, text = 'Register new Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        ttk.Button(frame, text = 'Save Product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)
        
        self.create_connection()

        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = row[1])

    def add_product(self):
        query = 'INSERT INTO product VALUES(?, ?)'
        parameters =  (self.name.get(), self.price.get())
        self.run_query(query, parameters)
        self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
        self.name.delete(0, END)
        self.price.delete(0, END)
        self.get_products()


if __name__ == '__main__':
#     Product.create_connection("database.db")
    window = tk.Tk()
    application = Product(window)
    window.mainloop()
