# Importando as bibliotecas necessárias
from selenium_funcs import selenium_start
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import schedule
import time
import matplotlib.pyplot as plt 
import json
from datetime import datetime
# Get the path to the "Documents" folder for the current user
documents_path = r'Z://config'



# Function to fetch values from the website and return a dictionary
def fetch_values():
    try:
        driver = selenium_start(config_path=documents_path,downloadfolder_path=documents_path,headless=False)
        driver.get('https://www.localiza.com/brasil/pt-br')
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.ID, 'mat-input-1').send_keys("Shop Boulevard Tatuape",Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'places-list__item__content')))
        driver.find_element(By.ID, 'mat-input-1').send_keys(Keys.DOWN,Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mat-calendar-next-button')))
        # Obter a data atual
        data_atual = datetime.now()

        # Verificar o mês atual
        mes_atual = data_atual.month

        # Localizar o botão de avanço do calendário
        botao_avanco = driver.find_element(By.CLASS_NAME, 'mat-calendar-next-button')

        # Determinar quantas vezes clicar com base no mês atual
        if mes_atual == 8:
            vezes_clicar = 2
        elif mes_atual == 9:
            vezes_clicar = 1
        else:
            vezes_clicar = 0

        # Clicar no botão o número de vezes necessário
        for _ in range(vezes_clicar):
            botao_avanco.click()
        driver.find_elements(By.CLASS_NAME, 'mat-calendar-body-cell')[13].click()
        wait.until(EC.presence_of_element_located((By.ID, 'mat-option-0')))
        driver.find_element(By.ID, 'mat-option-0').click()
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mat-calendar-body-cell')))
        driver.find_elements(By.CLASS_NAME, 'mat-calendar-body-cell')[15].click()
        sleep(.8)
        driver.find_element(By.CLASS_NAME,"ds-button").click()
        x = 0
        # Find all elements with class "fast-off" and "new-group-car-content-box-price-value__rate"
        for _ in range(3):
            fast_off_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'fast-off')))
            price_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'new-group-car-content-box-price-value__rate')))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(.5)

        # Create a dictionary to store the values of "fast-off" classes
        values_dict = {}

        # Extract the values from elements and store in the dictionary
        for i in range(len(fast_off_elements)):
            values_dict[fast_off_elements[i].get_attribute('innerText')] = price_elements[i].get_attribute('innerText')

        # Print the dictionary with the class values and corresponding prices
        print(values_dict)
        return values_dict
    
    finally:
        driver.quit()

def save_data_to_file(data, file_path):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_data_from_file(file_path):
    if not os.path.exists(file_path):
        # Create an empty JSON object if the file doesn't exist
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump({}, file, ensure_ascii=False)
    
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            file_content = file.read()
            return json.loads(file_content)
    except Exception as e:
        print("Error reading or parsing file:", e)
        return None

# Caminho para o arquivo onde os dados serão salvos e lidos
data_file_path = 'data.json'

def job():
    # Carrega os dados existentes do arquivo
    try:
        existing_data = load_data_from_file(data_file_path)
    except FileNotFoundError:
        existing_data = {}

    # Executa o código e obtém os valores coletados
    values_dict = fetch_values()

    # Adiciona os novos valores com a data/hora atual
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    existing_data[timestamp] = values_dict

    # Salva os valores atualizados no arquivo
    save_data_to_file(existing_data, data_file_path)

# Execute the job function
job()