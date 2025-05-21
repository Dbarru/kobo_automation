import pandas as pd 
import requests
import sqlite3

#connection to the database
conn = sqlite3.connect("your/path/to/calibre/ligtsql.db")

#create a cursor to execute SQL command
cursor = conn.cursor()

#select only the book's title and fetch them
cursor.execute("SELECT title FROM books")
books = cursor.fetchall()
lista_libri = []

#save the book's title in a list 
for book in books:
   lista_libri.append(book[0])
