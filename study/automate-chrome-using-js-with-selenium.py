import time # time.sleep(9)
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager

# Configuração do serviço do WebDriver
service = Service(ChromeDriverManager().install())

# Configuração do navegador Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Abrir navegador maximizado

# Inicialização do driver do Chrome
driver = webdriver.Chrome(service=service, options=options)

try:
    # Abrir uma página web
    driver.get("https://www.example.com")

    # Injetar e executar JavaScript no contexto da página
    script = '''
    // Exemplo de código JavaScript
    alert("Olá! Esta é uma mensagem de alerta injetada via Python e Selenium.");

    function sayHello(name) {
        console.log("Hello, " + name + "!");
    }

    // Chamando a função
    sayHello("Alice");
    '''
    driver.execute_script(script)
        # Aguardar por 3 segundos (ajuste conforme necessário)
    time.sleep(9)

finally:
    # Fechar o navegador
    print("finished")
