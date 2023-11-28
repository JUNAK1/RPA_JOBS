from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
import pyautogui
#import keyboard
pyautogui.click() 

PATH = 'C:/Users/USUARIO/Desktop/RPA/msedgedriver.exe'

edge_Options = Options()

edge_Options.accept_insecure_certs = True

edge_Service = Service(PATH)
browser = webdriver.Edge(service=edge_Service,options=edge_Options)

    # Navega al sitio de inicio de sesión
browser.get("http://ceadmclaro.clarochile.cl/indexTLV.html")



username_cu = "120495399"
password_cu = "JB9539"

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

#letras_mayusculas = [chr(i) for i in range(ord('A'), ord('Z')+1)]
letras_mayusculas = ['A']
list_comunas = ['LOS ANDES']

print(list_comunas)
conjuntos_por_comuna = []
# //*[@id="prosp_calle"]
comunasx = []

for comuna in list_comunas:                       
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
        try:
            desplegable2 = browser.find_element(By.ID,"prosp_calle")
            desplegable2.send_keys(letra)
            
            sleep(1)
            # Busca el elemento ul por clase en lugar de por ID
            ul_element_calle = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-autocomplete"))
            )
            li_elements_calle = ul_element_calle.find_elements(By.TAG_NAME, 'li')

            for li_calle in li_elements_calle:
                comunasx.append(li_calle.text)
                print(li_calle)

        except (NoSuchElementException,TimeoutException) as e:
            print("No se encontró el elemento desplegable: ", e)
            pass

        finally:
            sleep(3)
            desplegable2.clear()




browser.quit()
print('conjuntos_por_comuna: ',conjuntos_por_comuna)