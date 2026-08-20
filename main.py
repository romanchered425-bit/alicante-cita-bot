import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
NIE = os.environ["NIE"]
FULL_NAME = os.environ["FULL_NAME"]

URL = "https://icp.administracionelectronica.gob.es/icpplus/index.html"


def telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message},
        timeout=20,
    )


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1280,1000")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

try:
    print("Відкриваю ICPplus...")
    driver.get(URL)

    # 1. Провінція Alicante
    province = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#form")
        )
    )
    Select(province).select_by_visible_text("Alicante")

    driver.find_element(By.ID, "btnAceptar").click()

    # 2. Процедура TIE / huellas — код 4010
    procedure = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#divGrupoTramites select")
        )
    )
    Select(procedure).select_by_value("4010")

    driver.find_element(By.ID, "btnAceptar").click()

    # 3. Вхід без Cl@ve
    entrar = wait.until(
        EC.presence_of_element_located(
            (By.ID, "btnEntrar")
        )
    )
    driver.execute_script("arguments[0].click();", entrar)

    # 4. Дані заявника
    nie_field = wait.until(
        EC.presence_of_element_located((By.ID, "txtIdCitado"))
    )
    nie_field.clear()
    nie_field.send_keys(NIE)

    name_field = wait.until(
        EC.presence_of_element_located((By.ID, "txtDesCitado"))
    )
    name_field.clear()
    name_field.send_keys(FULL_NAME)

    driver.find_element(By.ID, "btnEnviar").click()

    # 5. Перевіряємо результат
    wait.until(lambda d: d.find_element(By.TAG_NAME, "body"))

    text = driver.find_element(By.TAG_NAME, "body").text

    if "no hay citas disponibles" in text.lower():
        print("Вільних записів немає.")
    elif "no hay suficientes" in text.lower():
        print("Вільних записів немає.")
    else:
        telegram(
            "🚨 З'ЯВИВСЯ ЗАПИС ALICANTE!\n\n"
            "TIE / TOMA DE HUELLAS (4010)\n\n"
            "Зайди на офіційний ICPplus і перевір дату та час."
        )
        print("🚨 Можливо, з'явився запис!")

finally:
    driver.quit()
