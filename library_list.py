import pandas as pd 
import requests
import sqlite3

# Connessione al database (crea il file se non esiste)
conn = sqlite3.connect("/home/barru/Biblioteca di calibre/metadata.db")

# Creazione di un cursore per eseguire comandi SQL
cursor = conn.cursor()

cursor.execute("SELECT title FROM books")
books = cursor.fetchall()
lista_libri = []

for book in books:
   lista_libri.append(book[0])

print(lista_libri)