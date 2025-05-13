import time
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np 
import pandas as pd 
from random import randint
from library_list import *

# Ottieni automaticamente il ChromeDriver corretto senza specificare la versione
driver_path = ChromeDriverManager().install()

# Avvia il browser in modalità UC con il ChromeDriver corretto
driver = uc.Chrome(driver_executable_path=driver_path, headless=False)
driver.get("https://www.kobo.com/it/en/library/books")

input('Premi Invio dopo aver effettuato l\'accesso')

numero_pagine = driver.find_element(By.CSS_SELECTOR, 'a.page-link.final')
ultima_pagina = int(numero_pagine.text)

titoli_final = []
status_finale = []
data_finale = []
generi_finale = []
serie_finale = []

def extract_info(riga, selector):
    try:
        elemento = riga.find_element(By.CSS_SELECTOR, selector).text
    except:
        elemento = None
    return elemento

# for pagina in range(ultima_pagina):
# time.sleep(5)
righe = driver.find_elements(By.CSS_SELECTOR, '.item-wrapper.book')
for riga in righe:
    try:
        titolo = extract_info(riga, '.title.product-field')
        if titolo not in lista_libri:
            button = riga.find_element(By.CLASS_NAME, "library-actions-trigger")
            driver.execute_script("arguments[0].click();", button)

            time.sleep(5)
            button_download = riga.find_element(By.CLASS_NAME, "library-action.export-file")
            driver.execute_script("arguments[0].click();", button_download)

            time.sleep(5)
            button_download2 = driver.find_element(By.CLASS_NAME, "primary-button.export")
            driver.execute_script("arguments[0].click();", button_download2)

            
        status = extract_info(riga,'.product-field.item-status')
        data = extract_info(riga,'.date-added.date-field')
        genere = extract_info(riga,'.genre.product-field')
        serie = extract_info(riga,'.series.product-field')

        titoli_final.append(titolo)
        status_finale.append(status)
        data_finale.append(data)
        generi_finale.append(genere)
        serie_finale.append(serie)
        time.sleep(randint(1,5))
        print(titolo)
    except Exception as e:  # Cattura l'errore specifico
        print(f'Errore alla pagina: {str(e)}')

    # time.sleep(randint(1,5))
    # next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next')))
    # next_button.click()
    # print(pagina)



