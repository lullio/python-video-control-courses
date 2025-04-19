import os
import platform

import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

import undetected_chromedriver as uc
from seleniumbase import Driver

from webdriver_manager.chrome import ChromeDriverManager

import requests
import csv
import json

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import keyboard
import re
import time
import threading

import pyuac


# Definindo a variável global
# video_tab = ""

def kill_chrome_processes():
    if platform.system() == 'Linux':
        os.system('pkill -f chrome')
    elif platform.system() == 'Windows':
        os.system('taskkill /im chrome.exe /f')
def kill_firefox_processes():
    if platform.system() == 'Linux':
        os.system('pkill -f firefox')
    elif platform.system() == 'Windows':
        os.system('taskkill /im firefox.exe /f')
        

# Configuração do serviço do WebDriver, driver chrome ou firefox
def setup_driver(browser="chrome"):
    if browser.lower() == "chrome":
        # Encerrar processos existentes do Chrome
        kill_chrome_processes()
        
        # Instalar e configurar o serviço do ChromeDriver
        # print(ChromeDriverManager().install())
        chrome_install = ChromeDriverManager().install()
        folder = os.path.dirname(chrome_install)
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
        service = ChromeService(chromedriver_path)
        
        
        # Configuração do navegador Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--profile-directory=Default")
        if os.name == 'nt':  # Windows
            options.add_argument("--user-data-dir=C:/Users/Felipe/AppData/Local/Google/Chrome/User Data")
        elif os.name == 'posix':  # Linux (inclui Pop!_OS)
            options.add_argument("--user-data-dir=/home/felipe/.config/google-chrome")
        # options.add_argument("--profile-directory=Default")
        driver = webdriver.Chrome(service=service, options=options)

    elif browser.lower() == "firefox":
        # Encerrar processos existentes do Firefox (se necessário)
        kill_firefox_processes()
        # Instalar e configurar o serviço do GeckoDriver
        geckodriver_path = GeckoDriverManager().install()
        service = FirefoxService(geckodriver_path)
        
        # Configuração do navegador Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")
        if os.name == 'nt':  # Windows
            profile_path = r"C:\Users\Felipe\AppData\Roaming\Mozilla\Firefox\Profiles\ibyn6bg1.default-release"
            options.set_preference("profile", profile_path)
            # Disfarçar a automação
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference("useAutomationExtension", False)
            options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")
            profile = webdriver.FirefoxProfile(profile_path)
            options.profile = profile
            driver = webdriver.Firefox(service=service, options=options)
        elif os.name == 'posix':  # Linux (inclui Pop!_OS)
            profile_path = "/home/felipe/.mozilla/firefox/your-profile"
            profile = webdriver.FirefoxProfile(profile_path)
            options.profile = profile
            driver = webdriver.Firefox(service=service, options=options)
        
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver
# Configuração do serviço do WebDriver, driver google chrome
def setup_driver_oficial():
    # Encerrar processos existentes do Chrome
    kill_chrome_processes()
    
    # Instalar e configurar o serviço do ChromeDriver
    # driver_path = ChromeDriverManager().install()
    # print(f"ChromeDriver path: {driver_path}")  # Debug: Verifique o caminho do ChromeDriver
    # service = Service(driver_path)
    # service = Service(ChromeDriverManager().install())
    
    # Solve: OSError: [WinError 193] %1 is not a valid Win32 application
    # https://stackoverflow.com/questions/78796828/i-got-this-error-oserror-winerror-193-1-is-not-a-valid-win32-application
    
    # Instalar e configurar o serviço do ChromeDriver
    chrome_install = ChromeDriverManager().install()
    
    folder = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder, "chromedriver.exe")

    service = ChromeService(chromedriver_path)
    
    
    # Configuração do navegador Chrome
    options = webdriver.ChromeOptions()
    
    # Abrir navegador maximizado
    options.add_argument("--start-maximized")
    # Detectar o sistema operacional e definir o diretório de dados do usuário do Chrome
    if os.name == 'nt':  # Windows
        options.add_argument("--user-data-dir=C:/Users/Felipe/AppData/Local/Google/Chrome/User Data")
        options.add_argument("--profile-directory=Default")  # Ajuste se necessário
    elif os.name == 'posix':  # Linux (inclui Pop!_OS)
        options.add_argument("--user-data-dir=/home/felipe/.config/google-chrome")
        options.add_argument("--profile-directory=Profile 4")  # Ajuste se necessário
    # Diretório do perfil padrão chrome no windows
    #options.add_argument("--user-data-dir=C:/Users/Felipe/AppData/Local/Google/Chrome/User Data")
    # Diretório do perfil padrão chrome no popos
    #options.add_argument("--user-data-dir=/home/felipe/.config/google-chrome/Profile 4") # PopOS perfil propz
    
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    #options.add_argument("--remote-allow-origins=*")  # Permitir todas as origens remotas
    #options.add_argument("--window-size=1920,1080")
    #options.add_argument("--headless") # executar chrome sem interface gráfica
    #options.add_argument("--disable-extensions")
    #options.add_argument("--disable-notifications")
    #options.add_argument("--disable-gpu")
    #options.add_argument("--ignore-certificate-errors")
    #options.add_argument("--disable-popup-blocking")  # Desabilita o bloqueio de pop-ups
    #options.add_argument("--disable-infobars")  # Desabilita as infobars
    #options.add_argument("--no-first-run")  # Não executa a primeira execução
    #options.add_argument("--no-sandbox")  # Nenhum ambiente de laboratório
    #options.add argument ("--remote-debugging-port=0")
    
    # Inicialização do driver do Chrome
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Encerrar o navegador
    #driver.quit()
    return driver

def spreadsheet():
    webbrowser.open("https://docs.google.com/spreadsheets/d/1Fg4cP6VEjQ5Ke8LCTSo88dUdZlc1az2RpBC6Bu6YuSw/edit?usp=sharing")
def udemy():
    webbrowser.open("https://www.udemy.com/home/my-courses/learning/")
def about():
    webbrowser.open("https://projetos.lullio.com.br/gerenciador-de-cursos-e-controle-de-video")
    webbrowser.open("https://github.com/lullio/python-video-control-courses")
    
# Função para abrir a nova GUI de configurações
def open_config_window():
    def save_config():
        config = {
            'sheet_link': sheet_link_var.get(),
            'sheet_name': sheet_name_var.get(),
            'export_type': export_type_var.get(),
            'data_range': data_range_var.get(),
            'query': query_var.get("1.0", "end-1c")
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        messagebox.showinfo("Configuração", "Configurações salvas com sucesso!")
        config_window.destroy()
    
    # Cria a nova janela
    config_window = tk.Toplevel(root)
    config_window.title("Configurações de Planilha e Exportação")
    config_window.geometry("400x300")

    # Combobox para o link da planilha
    tk.Label(config_window, text="Link da Planilha:").pack(pady=(10, 0))
    sheet_link_var = tk.StringVar()
    sheet_link_combobox = ttk.Combobox(config_window, textvariable=sheet_link_var, width=50)
    sheet_link_combobox.pack(pady=(0, 10))
    # Adicione opções de exemplo, ou permita o usuário colar a URL
    sheet_link_combobox['values'] = ("Planilha 1", "Planilha 2")

    # Campo de texto para o nome ou ID da planilha/worksheet
    tk.Label(config_window, text="Nome ou ID da Planilha / Worksheet:").pack(pady=(10, 0))
    sheet_name_var = tk.StringVar()
    sheet_name_entry = tk.Entry(config_window, textvariable=sheet_name_var, width=50)
    sheet_name_entry.pack(pady=(0, 10))

    # Combobox para tipos de exportação e campo de texto para range de dados
    tk.Label(config_window, text="Tipo de Exportação e Range de Dados:").pack(pady=(10, 0))
    export_type_var = tk.StringVar()
    export_type_combobox = ttk.Combobox(config_window, textvariable=export_type_var, values=("csv", "json"), width=20)
    export_type_combobox.pack(side="left", padx=(0, 10))
    data_range_var = tk.StringVar()
    data_range_entry = tk.Entry(config_window, textvariable=data_range_var, width=30)
    data_range_entry.pack(side="left")

    # Campo de texto para a query
    tk.Label(config_window, text="Query:").pack(pady=(10, 0))
    query_var = tk.Text(config_window, width=50, height=3)
    query_var.pack(pady=(0, 10))

    # Botão de salvar
    save_button = tk.Button(config_window, text="Salvar", command=save_config)
    save_button.pack(pady=(10, 10))

# Função para carregar as configurações do arquivo JSON
def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
        sheet_link_var.set(config.get('sheet_link', ''))
        sheet_name_var.set(config.get('sheet_name', ''))
        export_type_var.set(config.get('export_type', 'csv'))
        data_range_var.set(config.get('data_range', ''))
        query_var.delete('1.0', 'end')
        query_var.insert('1.0', config.get('query', ''))
        
def get_data_from_google_sheet(url_data, driver):
    global root
    global sheet_link_var
    global sheet_name_var
    global export_type_var
    global data_range_var
    global query_var
    try:
        # Realiza uma requisição GET para obter o conteúdo da planilha
        response = requests.get(url_data)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        # OU
         # Verifica se a requisição foi bem-sucedida (código 200)
        #if response.status_code == 200:
    except requests.RequestException as e:
        print(f"Erro ao obter dados da planilha: {e}")
        return None

    # Lê o conteúdo CSV retornado pela API do Google Sheets
    csv_data = response.text
    print(csv_data)
    # Utiliza o módulo csv para ler os dados CSV
    csv_reader = csv.reader(csv_data.splitlines())

    # Criação da janela principal
    root = tk.Tk()
    root.title("Gerenciador de Cursos - Felipe")
    root.attributes('-topmost', True)
    
    # Configurar a fonte para os itens da Treeview
    style = ttk.Style()
    # style.configure("Treeview", font=("Helvetica", 12))  # Aumentar o tamanho da fonte
    # style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))  # Fonte maior para cabeçalhos

    # Configurar o espaçamento das linhas
    if os.name == 'posix': # somente no Linux
        style.configure("Treeview", rowheight=40)  # Aumentar a altura das linhas

    
    # Criação da barra de menu
    menu_bar = tk.Menu(root)

    # Menu Arquivo
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Planilha", command=spreadsheet)
    # file_menu.add_separator()
    file_menu.add_command(label="Udemy", command=udemy)
    menu_bar.add_cascade(label="Abrir", menu=file_menu)

    # Menu Editar
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Editar", menu=file_menu)
    file_menu.add_command(label="Trocar Planilha e Configurações", command=open_config_window)
    
    # Menu Ajuda
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Sobre", command=about)
    help_menu.add_separator()
    help_menu.add_command(label="Shift+L = Pause/Play", command=about)
    help_menu.add_command(label="Shift+= = Aumentar velocidade", command=about)
    help_menu.add_command(label="Shift+- = Diminuir velocidade", command=about)
    help_menu.add_separator()
    help_menu.add_command(label="Shift+< = Retroceder", command=about)
    help_menu.add_command(label="Shift+> = Avançar", command=about)
    help_menu.add_command(label="Shift+k = Legenda", command=about)
    help_menu.add_command(label="Shift+Home = Vídeo Anterior", command=about)
    help_menu.add_command(label="Shift+End = Próximo Vídeo", command=about)
    help_menu.add_separator()
    help_menu.add_command(label="Shift+ x = Test alert()", command=about)
    help_menu.add_command(label="Sobre", command=about)
    menu_bar.add_cascade(label="Ajuda", menu=help_menu)
    
    # Adicionar a barra de menu à janela principal
    root.config(menu=menu_bar)
    
    # Carregar configurações ao iniciar
    sheet_link_var = tk.StringVar()
    sheet_name_var = tk.StringVar()
    export_type_var = tk.StringVar()
    data_range_var = tk.StringVar()
    query_var = tk.Text(root, width=50, height=3)
    load_config()
    

     # Criando uma ListView com scroll vertical
    tree = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"), show="headings")
    tree.heading("col1", text="Index")
    tree.heading("col2", text="Cursos")
    tree.heading("col3", text="URL")
    tree.heading("col4", text="Categorias")
    tree.heading("col5", text="Plataforma")
    tree.heading("col6", text="URL Notion")
    tree.heading("col7", text="É Favorito")
    tree.heading("col8", text="Em Andamento")
    # tree.heading("col9", text="Avaliação do Curso")
    # tree.heading("col10", text="Carga Horária(h)")
    tree.pack(fill="both", expand=True)
    
    # Lista para armazenar todas as linhas do CSV
    all_rows = []
    # Conjunto para armazenar valores únicos da coluna 4 (categorias dos cursos)
    unique_col4_values = set()
    # Listas para armazenar linhas com True nas colunas 6(favorito) e 7(em andamento)
    favorites_rows = []
    in_progress_rows = []
    # Variáveis para verificar se existem valores True nas colunas 6 e 7
    favorites_exist = False
    in_progress_exist = False
    

    # Itera sobre as linhas do CSV
    for row in csv_reader:
         # Inserir cada linha na ListView
        tree.insert("", "end", values=row)
        # salvar linhas do csv na var/lista all_rows 
        all_rows.append(row)
        # salvar os valores da coluna 4 na lista unique_col4_values
        unique_col4_values.add(row[3])
        
        # Verificar se a linha tem pelo menos 8 elementos
        if len(row) > 7:
            if row[6].lower() == 'true':
                favorites_rows.append(row)
                favorites_exist = True
            if row[7].lower() == 'true':
                in_progress_rows.append(row)
                in_progress_exist = True
        else:
            print("A linha não tem mais de 7 colunas, verifique a url da planilha e altere o range")
        # Ajustar os valores para o filtro do ComboBox
        if favorites_exist:
            unique_col4_values.add("Favoritos")
        if in_progress_exist:
            unique_col4_values.add("Em Andamento")
            
        if favorites_exist:
            unique_col4_values.add("Favoritos")
        if in_progress_exist:
            unique_col4_values.add("Em Andamento")
        
    # Ajustando a largura das colunas
    for col in tree["columns"]:
        # Define largura mínima e colocar o conteúdo na esquerda(="w") ou centraliza conteúdo(CENTER)
        tree.column(col, width=1, minwidth=0, anchor="w")
        # Centraliza o texto do cabeçalho
        tree.heading(col, anchor="w")
    if os.name == "nt": # somente no windows
        tree.column(0, width=50, minwidth=50, anchor="w")
        tree.column(1, width=350, minwidth=350, anchor="w")
    elif os.name == 'posix': # somente no linux
        tree.column(0, width=100, minwidth=100, anchor="w")
        tree.column(1, width=800, minwidth=780, anchor="w")

    frame = tk.Frame(root)
    frame.pack(padx=5, pady=10)

    # Dropdown para filtrar por valores da coluna 4
    col4_filter_label = tk.Label(frame, text="Filtrar por Categoria:")
    col4_filter_label.grid(row=0, column=0, padx=(0, 10), sticky="w", pady=10)

    # Atualiza a lista de valores do ComboBox
    col4_values = sorted(list(unique_col4_values)) 
    col4_filter_var = tk.StringVar(root)
    
    # Define o valor padrão do combobox como "Em Andamento"
    col4_filter_var.set("Em Andamento") 
    

    col4_filter_dropdown = ttk.Combobox(frame, textvariable=col4_filter_var, values=["Todos"] + col4_values, state="readonly", width=27)
    col4_filter_dropdown.grid(row=0, column=1, sticky="w")

    search_label = tk.Label(frame, text="Pesquisar:")
    search_label.grid(row=1, column=0, padx=(0, 10), sticky="w")

    search_var = tk.StringVar()
    search_entry = tk.Entry(frame, textvariable=search_var, width=30)
    search_entry.grid(row=1, column=1, sticky="we", padx=(0, 10))

    # Função para filtrar os dados da Treeview com base no valor selecionado no dropdown
    def filter_data_with_combobox(event=None):
        selected_value = col4_filter_var.get() # recupera o texto/valor do combobox
        tree.delete(*tree.get_children()) # Limpa a Treeview antes de aplicar o filtro
        # Mostra todas as linhas se "Todos" estiver selecionado
        if selected_value == "Todos":
            for row in all_rows:
                tree.insert("", "end", values=row)
        elif selected_value == "Favoritos":
                for row in favorites_rows:
                    tree.insert("", "end", values=row)
        elif selected_value == "Em Andamento":
                for row in in_progress_rows:
                    tree.insert("", "end", values=row)                
        else:
            # Filtra as linhas com base no valor selecionado na coluna 4
            filtered_rows = [row for row in all_rows if row[3] == selected_value]
            for row in filtered_rows:
                tree.insert("", "end", values=row)
    # Liga o evento de seleção do combobox
    col4_filter_dropdown.bind("<<ComboboxSelected>>", filter_data_with_combobox)
    # Atualiza a Treeview com base no filtro padrão
    filter_data_with_combobox()

    def filter_data_with_search(event=None):
        query = search_var.get()
        tree.delete(*tree.get_children()) # Limpa a Treeview antes de aplicar o filtro
        try:
            regex = re.compile(query, re.IGNORECASE) # Regex case insensitive
            for row in all_rows:
                if any(regex.search(str(value)) for value in row):
                    tree.insert("", "end", values=row)
        except re.error:
            pass

    # Liga o evento de seleção do combobox
    search_var.trace_add("write", lambda *args: filter_data_with_search())

    # Função para lidar com o clique duplo na ListView
    def on_item_click(event):
        item = tree.selection()[0]
        if item:
            # Obtém os valores da linha clicada
            values = tree.item(item, "values")
            # Abre o navegador com o link da coluna 3 (índice 2)
            driver.get(values[2]) # Coluna 3 = url do curso usando selenium pois quero abrir no meu perfil Felipe do Chrome
            # Abrir Notion
            webbrowser.open(values[5]) # Coluna 6 = url do notion
            # video_tab = driver.current_window_handle
    # Define o evento de duplo clique na ListView
    tree.bind("<Double-1>", on_item_click)
    
    # Iniciar o loop principal da GUI
    root.mainloop()

def pause_and_play_video(driver):
    # Alterna para a aba do vídeo
    # driver.switch_to.window(video_tab)
    print("URL atual:", driver.current_url)

    js_play_video = '''
        var videoElem = document.querySelectorAll('video')[0];
        //videoElem.muted = true;
        
        async function playVideo() {
            try {
                //Simular a interação do usuário para permitir reprodução automática
                var clickEvent  = document.createEvent ('MouseEvents');
                clickEvent.initEvent ('click', true, true);
                videoElem.dispatchEvent (clickEvent);
                document.body.dispatchEvent (clickEvent)
                
                await videoElem.play();
                //videoElem.muted = false;
            } catch (err) {
                console.log(err)
            }
        }
        if(videoElem.paused){
            // método alternativo, clicar no botão play
             var clickEvent  = document.createEvent ('MouseEvents');
            clickEvent.initEvent ('click', true, true);
            document.querySelectorAll('[data-purpose="play-button"]')[0]?.dispatchEvent (clickEvent);
            playVideo();
        } else {
            videoElem.pause();
            // método alternativo, clicar no botão pause
            document.querySelectorAll('[data-purpose="pause-button"]')[0]?.click();
        }   
        if(videoElem){
            videoElem.onplay = (e) => {
                e.target.playbackRate = localStorage.getItem('videoSpeed');
            }
        }
    '''
    driver.execute_script(js_play_video)

# def change_video_speed(driver, increase=True):
#     js_change_speed = f'''
#     var video = document.getElementsByTagName('video')[0];
#     function speed(value) {{
#         video.playbackRate += value;
#     }}
#     if({increase}) {{
#         speed(0.25);
#     }} else {{
#         speed(-0.25);
#     }}
#     localStorage.setItem('videoSpeed', video.playbackRate);
#     '''
#     driver.execute_script(js_change_speed)

def increase_video_speed(driver):
    print("URL atual:", driver.current_url)

    js_increase_speed = '''
// capturar o video
{
var video = document.getElementsByTagName('video')[0];

// aumentar velocidade do video
function speed(value = 0.15) {
  video.playbackRate += value;
}
if(video.playbackRate <=4.0){ // para não dar erro, executar somente se a velocidade for menor ou igual a 4
  speed(); // executar função
  console.log("aumentei a velocidade: ", video.playbackRate);
  localStorage.setItem('videoSpeed', video.playbackRate);
}
}
'''
    driver.execute_script(js_increase_speed)
    
def decrease_video_speed(driver):
    js_decrease_speed = '''
// capturar o video

var video = document.getElementsByTagName('video')[0];

// diminuir velocidade do video
function speed(value = 0.15) {
  video.playbackRate -= value;
  video.defaultPlaybackRate -= value;
}
if(video.playbackRate >= 0.15){ // para não dar erro , só executar se a velocidade do video for maior ou igual a 0.25
  speed(); // executar função
  console.log("diminui a velocidade: ", video.playbackRate);
  localStorage.setItem('videoSpeed', video.playbackRate);
}
'''
    driver.execute_script(js_decrease_speed)
    
def fast_forward_video(driver):
    print("URL atual:", driver.current_url)

    js_fast_forward = '''
    var video = document.getElementsByTagName('video')[0];
    function skip(value) {
        video.currentTime += value;
    }
    skip(3);
    '''
    driver.execute_script(js_fast_forward)
def teste(driver):
    print("URL atual:", driver.current_url)

    js_test = '''
alert('teste')
    '''
    driver.execute_script(js_test)

def rewind_video(driver):
    print("URL atual:", driver.current_url)

    js_rewind_video = '''
    var video = document.getElementsByTagName('video')[0];
    function rewind(value) {
        video.currentTime -= value;
    }
    rewind(3);
    '''
    driver.execute_script(js_rewind_video)
    
def next_video(driver):
    print("URL atual:", driver.current_url)

    js_skip_video = '''
var goNext = document.querySelectorAll('#go-to-next-item')[0];
var clickEvent  = document.createEvent ('MouseEvents');
clickEvent.initEvent ('click', true, true);

// avançar pro próximo vídeo
goNext.dispatchEvent (clickEvent);
//goNext.click();
    '''
    driver.execute_script(js_skip_video)
def back_video(driver):
    print("URL atual:", driver.current_url)

    js_back_video = '''
var goPrevious = document.querySelectorAll('#go-to-previous-item')[0];
var clickEvent  = document.createEvent ('MouseEvents');
clickEvent.initEvent ('click', true, true);

// voltar pro video anterior
goPrevious.dispatchEvent (clickEvent);
//goPrevious.click();
    '''
    driver.execute_script(js_back_video)

def toggle_video_subtitles(driver):
    print("URL atual:", driver.current_url)

    js_toggle_subtitles = '''
{
		// clicar no legenda
	document.querySelectorAll('[aria-label="Legendas"], [aria-label="Subtitles"]')[0]?.parentElement?.parentElement?.click();
	console.log("click legend icon")
	var optionDesligado;
    var optionIngles;
			// selecionar desligado ou ingles
	var selectionsAtive = document.querySelectorAll('[aria-checked="true"]');
    var allOptions = document.querySelectorAll('ul[aria-label="Legendas"] li, ul[aria-label="Subtitles"] li, ul[aria-label="Captions"] li');
    allOptions.forEach(val => {
        if(val?.textContent?.includes('Ingl') || val?.textContent?.includes('English')){
            optionIngles = val;
        }else if(val.textContent.includes('Deslig') || val.textContent.includes('Off')){
            optionDesligado = val;
        }
    })
    if(optionDesligado?.firstChild?.getAttribute('aria-checked') == 'true'){
        optionIngles?.firstChild?.firstChild?.click();
    }else{
        optionDesligado?.firstChild?.firstChild?.click();
    }



	// document.querySelectorAll('[aria-label="Legendas"]')[0].parentElement.parentElement.click();
	// console.log("click legend icon")
	
	// 		// selecionar desligado ou ingles
	// let selectionsAtive = document.querySelectorAll('[aria-checked="true"]');
	// selectionsAtive.forEach(val => {
	// 	if(val.textContent.includes("Desligado")){
	// 		// selecionar ingles
	// 		document.querySelectorAll('[aria-checked="true"')[1].closest('li').nextElementSibling.nextElementSibling.firstChild.click();
	// 		console.log("legenda: ingles selecionado")
	// 	}else if(val.textContent.includes("Ingl")){
	// 		// selecionar desligado
	// 			document.querySelectorAll('[aria-checked="true"')[1].closest('li').previousSibling.previousSibling.firstChild.firstChild.click();
	// 			console.log("legenda: desabilitado selecionado")
	// 	}
	// })
}
    '''
    driver.execute_script(js_toggle_subtitles)

# Função para associar as hotkeys
def start_keyboard_shortcuts(driver):
    keyboard.add_hotkey('shift+l', lambda: pause_and_play_video(driver), suppress=True)
    keyboard.add_hotkey('shift+x', lambda: teste(driver), suppress=True)
    keyboard.add_hotkey('shift+=', lambda: increase_video_speed(driver), suppress=True)
    keyboard.add_hotkey('shift+-', lambda: decrease_video_speed(driver), suppress=True)
    keyboard.add_hotkey('shift+left', lambda: rewind_video(driver), suppress=True)
    keyboard.add_hotkey('shift+right', lambda: fast_forward_video(driver), suppress=True)
    keyboard.add_hotkey('shift+end', lambda: back_video(driver), suppress=True)
    keyboard.add_hotkey('shift+home', lambda: next_video(driver), suppress=True)
    # keyboard.add_hotkey('shift+end', lambda: driver.execute_script("document.querySelector('#go-to-next-item')?.click();"))
    # keyboard.add_hotkey('shift+home', lambda: driver.execute_script("document.querySelector('#go-to-previous-item')?.click();"))
    keyboard.add_hotkey('shift+k', lambda: toggle_video_subtitles(driver), suppress=True)

    keyboard.wait('ctrl+shift+esc')

def main():
    driver = setup_driver()
    # URL da planilha do Google Sheets
    url_data = "https://docs.google.com/spreadsheets/d/1Fg4cP6VEjQ5Ke8LCTSo88dUdZlc1az2RpBC6Bu6YuSw/gviz/tq?tqx=out:csv&range=A2:H150&sheet=Cursos"

    # Inicie a GUI do Tkinter em uma thread separada
    gui_thread = threading.Thread(target=get_data_from_google_sheet, args=(url_data, driver))
    gui_thread.start()

    # Inicie as hotkeys do tecladoX
    start_keyboard_shortcuts(driver)

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:
        main()
