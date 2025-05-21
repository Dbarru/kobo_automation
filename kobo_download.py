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
from library_list import *  # Import a predefined list of books for comparison

# Automatically download and install the correct ChromeDriver version
driver_path = ChromeDriverManager().install()

# Launch an undetected Chrome browser to bypass anti-bot detection
driver = uc.Chrome(driver_executable_path=driver_path, headless=False)

# Open the Kobo library webpage
driver.get("https://www.kobo.com/it/en/library/books")

# Pause execution until the user manually logs in
input('Premi Invio dopo aver effettuato l\'accesso')

# Find the last page number in the library
numero_pagine = driver.find_element(By.CSS_SELECTOR, 'a.page-link.final')
ultima_pagina = int(numero_pagine.text)  # Convert extracted page number to an integer

# Lists to store extracted book information
titoli_final, status_finale, data_finale, generi_finale, serie_finale = [], [], [], [], []

# Function to extract text content from an element safely
def extract_info(riga, selector):
    try:
        elemento = riga.find_element(By.CSS_SELECTOR, selector).text  # Try retrieving text
    except:
        elemento = None  # If the element is missing, return None
    return elemento

# Loop through all pages in the library
for pagina in range(ultima_pagina):
    time.sleep(5)  # Pause to simulate human behavior
    righe = driver.find_elements(By.CSS_SELECTOR, '.item-wrapper.book')  # Locate all book items

    for riga in righe:
        try:
            # Extract book details using the helper function
            titolo = extract_info(riga, '.title.product-field')

            # Check if the book is already in the predefined list
            if titolo not in lista_libri:
                button = riga.find_element(By.CLASS_NAME, "library-actions-trigger")
                driver.execute_script("arguments[0].click();", button)  # Click "Actions" button

                time.sleep(5)  # Wait before proceeding
                button_download = riga.find_element(By.CLASS_NAME, "library-action.export-file")
                driver.execute_script("arguments[0].click();", button_download)  # Click "Download" button

                time.sleep(5)  # Wait again before the next step
                button_download2 = driver.find_element(By.CLASS_NAME, "primary-button.export")
                driver.execute_script("arguments[0].click();", button_download2)  # Click final confirmation

            # Extract additional book metadata
            status = extract_info(riga, '.product-field.item-status')
            data = extract_info(riga, '.date-added.date-field')
            genere = extract_info(riga, '.genre.product-field')
            serie = extract_info(riga, '.series.product-field')

            # Append extracted data to lists
            titoli_final.append(titolo)
            status_finale.append(status)
            data_finale.append(data)
            generi_finale.append(genere)
            serie_finale.append(serie)

            time.sleep(randint(1,5))  # Randomized pause to prevent detection
            print(titolo)  # Print extracted title for reference

        except Exception as e:  # Catch errors and display messages for debugging
            print(f'Errore alla pagina: {str(e)}')

    time.sleep(randint(1,5))  # Pause before navigating to the next page
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next')))
    next_button.click()  # Click "Next page" button
    print(pagina)  # Print current page number

driver.quit()

# Convert extracted data into a Pandas DataFrame for structured storage
info_finali = pd.DataFrame({'titolo': titoli_final,
                            'status': status_finale,
                            'data': data_finale,
                            'genere': generi_finale,
                            'serie': serie_finale})
