# Especificar la ruta al chromedriver
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import json
import pyautogui
import keyboard
pyautogui.click() 

PATH = 'C:/Users/crist/OneDrive/Escritorio/Scraper_counas/msedgedriver.exe'

edge_Options = Options()

edge_Options.accept_insecure_certs = True

edge_Service = Service(PATH)
browser = webdriver.Edge(service=edge_Service,options=edge_Options)

    # Navega al sitio de inicio de sesión
browser.get("http://ceadmclaro.clarochile.cl/indexTLV.html")




try:
    # Esperar y escribir en el campo de usuario
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='username']")))
        username_field = browser.find_element(By.XPATH, "//*[@id='username']")
        username_field.send_keys(username_cu)

        # Esperar y escribir en el campo de contraseña
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='password']")))
        password_field = browser.find_element(By.XPATH, "//*[@id='password']")
        password_field.send_keys(password_cu)

        # Enviar "Enter" y esperar a que la nueva página cargue
        password_field.send_keys(Keys.RETURN)
        sleep(3)
    
        boton = browser.find_element(By.XPATH,"//*[@id='servicios']/ul/li[2]/a")
        boton.click()

        sleep(3)
        boton_new_contract = browser.find_element(By.XPATH,"//*[@id='hfc']/div[1]/a")
        boton_new_contract.click()

        sleep(3)
        letras_mayusculas = [chr(i) for i in range(ord('A'), ord('C')+1)]
        #letras_mayusculas = [chr(i) for i in range(ord('A'), ord('Z')+1)]

        comunas = set()
        for letra in letras_mayusculas:
            desplegable = browser.find_element(By.ID,"prosp_comuna")
            desplegable.send_keys(letra)
            sleep(1)
            ul_element = browser.find_element(By.ID,"ui-id-1")

            li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

            for  li in li_elements:
                comunas.add(li.text)
            
            desplegable.clear()
        sleep(2)
        list_comunas = list(comunas)

        #Recortar list_comunas para test
        list_comunas = list_comunas[:3]
        print(list_comunas)
        conjuntos_por_comuna = {}
        # //*[@id="prosp_calle"]
        print("Step1")
        for comuna in list_comunas:
            
            comunasx = set()
            desplegable = browser.find_element(By.ID,"prosp_comuna")
            desplegable.clear()
            desplegable.send_keys(comuna)
            print("comuna: ",comuna)
            pyautogui.click()
            # Presionar la tecla flecha arriba
            pyautogui.press('up')

            # Presionar la tecla Enter
            pyautogui.press('enter')
            
            sleep(2)
            for letra in letras_mayusculas:
                desplegable2 = browser.find_element(By.ID,"prosp_calle")
                desplegable2.send_keys(letra)
                print("letra: ", letra)
                ul_element = browser.find_element(By.ID,"ui-id-1")
                li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
                print("x")
                #desplegable2.clear()

                calles = [opcion.text for opcion in li_elements if opcion != ""]
                conjuntos_por_comuna[comuna] = [comuna] + calles

                # Guardar el conjunto en el diccionario con la letra como clave
                
                print("2")
                desplegable2.clear()
                
        sleep(5)

except TimeoutException:
        print("Tiempo de espera excedido")
        raise TimeoutException

finally: 
       #browser.quit()
       print('###')
       #print(list_comunas)

       # Ahora puedes acceder a los conjuntos por cada letra del abecedario
       for letra, conjunto in conjuntos_por_comuna.items():
            print(f"Conjunto para la letra {letra}: {conjunto}")
            
with open('archivo_salida', 'w') as file_json:
    json.dump(conjuntos_por_comuna, file_json, ensure_ascii=False, indent=4)




            