from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import json
from time import sleep


# ABRE EL SISTEMA DE CONSULTA DE DIRECCION ENTEL
def abrir_cobertura_unificada(username_cu, password_cu):
    global browser

    # Especificar la ruta al chromedriver
    chrome_driver_path = 'C:\\Users\\Usuariooo\\.wdm\\drivers\\chromedriver\\win64\\119.0.6045.105\\chromedriver-win32\\chromedriver.exe'

    # Inicializar el navegador con la ruta especificada usando Service
    service = Service(chrome_driver_path)
    browser = webdriver.Chrome(service=service)

    # Navega al sitio de inicio de sesión
    browser.get("https://coberturaunificada.entel.cl/fugui-v2/#/login")

    try:
        # Esperar y escribir en el campo de usuario
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='username']")))
        username_field = browser.find_element(By.XPATH, "//*[@id='username']")
        username_field.send_keys(username_cu)

        # Esperar y escribir en el campo de contraseña
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='password']")))
        password_field = browser.find_element(By.XPATH, "//*[@id='password']")
        password_field.send_keys(password_cu)

        # Enviar "Enter" y esperar a que la nueva página cargue
        password_field.send_keys(Keys.RETURN)

        # Esperar a que el elemento específico esté presente
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Cobertura Unificada')]"))
        )

        # Navegar a la nueva URL en la misma pestaña
        nueva_url = "https://coberturaunificada.entel.cl/fugui-v2/#/cobertura/empresa"
        browser.get(nueva_url)

        print("Sistema de Cobertura Unificada abierto correctamente.")

    except TimeoutException:
        print("Tiempo de espera excedido")
        raise TimeoutException

# ESPERA A QUE LA ANIMACION DE "CARGANDO" NO EXISTA
def esperar_carga_completa(browser, clase_animacion, intervalo=0.5, timeout=30):
    """
    Espera hasta que la animación de carga especificada desaparezca.

    :param browser: Instancia del navegador Selenium.
    :param clase_animacion: Clase CSS de la animación de carga.
    :param intervalo: Tiempo en segundos entre cada verificación.
    :param timeout: Tiempo máximo en segundos para esperar.
    :return: None
    """
    tiempo_esperado = 0
    while tiempo_esperado < timeout:
        try:
            elemento = browser.find_element(By.CLASS_NAME, clase_animacion)
            if elemento.is_displayed():
                sleep(intervalo)
                tiempo_esperado += intervalo
            else:
                return
        except (NoSuchElementException, StaleElementReferenceException):
            # Si no se encuentra el elemento o si es obsoleto, significa que la carga ha terminado
            return
    raise TimeoutException(f"La animación de carga no desapareció después de {timeout} segundos.")

# BUSCA LA DIRECCION
def procesar_regiones(browser, archivo_json, archivo_salida):
    with open(archivo_json, 'r') as file:
        regiones_comunas = json.load(file)

    regiones_comunas_calles = {}

    for region, comunas in regiones_comunas.items():
        comunas_calles = {}
        # Seleccionar región

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//mat-select[@placeholder='Region']")))

        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//mat-select[@placeholder='Region']"))).click()

        campo_busqueda_region = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Buscar']")))

        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Buscar']")))

        campo_busqueda_region.clear()
        campo_busqueda_region.send_keys(region)
        sleep(.2)
        campo_busqueda_region.send_keys(Keys.RETURN)

        for comuna in comunas:
            if comuna:  # Asegurar que la comuna no esté vacía
                try:
                    # Espera a que la animación de carga desaparezca
                    sleep(1)
                    esperar_carga_completa(browser, 'overlay')

                    # Seleccionar comuna

                    WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//mat-select[@placeholder='Comuna']")))

                    WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//mat-select[@placeholder='Comuna']"))).click()

                    campo_busqueda_comuna = WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Buscar']")))

                    WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Buscar']")))

                    campo_busqueda_comuna.clear()
                    campo_busqueda_comuna.send_keys(comuna)
                    sleep(.2)
                    campo_busqueda_comuna.send_keys(Keys.RETURN)

                    # Espera a que la animación de carga desaparezca
                    sleep(1)
                    esperar_carga_completa(browser, 'overlay')

                    # Seleccionar calles
                    WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//mat-select[@placeholder='Calle']")))

                    WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//mat-select[@placeholder='Calle']"))).click()

                    opciones_calles = WebDriverWait(browser, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//mat-option")))

                    calles = [opcion.text for opcion in opciones_calles]

                    comunas_calles[comuna] = [comuna] + calles

                    # Cerrar el menú de calles
                    body = browser.find_element(By.TAG_NAME, 'body')
                    body.send_keys(Keys.ESCAPE)
                    sleep(.5)

                except TimeoutException:
                    print(f"No se pudieron procesar las calles para la comuna: {comuna}")

        regiones_comunas_calles[region] = comunas_calles

    # Escribir los datos en un archivo JSON
    with open(archivo_salida, 'w') as file_json:
        json.dump(regiones_comunas_calles, file_json, ensure_ascii=False, indent=4)

abrir_cobertura_unificada("isc_rlopetegui", "Clubvalpo.2024")
procesar_regiones(browser, 'comunas_por_region.json', 'comunas_por_region_con_calles.json')
