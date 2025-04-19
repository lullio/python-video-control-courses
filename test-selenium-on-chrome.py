from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # A opção abaixo faz abrir o chrome com modo de seleção de perfil
    # options.add_argument("--user-data-dir=C:/Users/Felipe/AppData/Local/Google/Chrome/User Data")
    
    # NÃO usar perfis personalizados
    # options.add_argument("--user-data-dir=C:/temp/selenium-profile")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    driver.get("https://example.com")
    time.sleep(12)

    try:
        driver.execute_script("alert('✅ Selenium funcionando!');")
        time.sleep(15)
        print("executou")
    except Exception as e:
        print(f"❌ ERRO ao executar script JS: {e}")

    return driver

driver = setup_driver()
