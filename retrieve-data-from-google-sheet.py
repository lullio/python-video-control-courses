import os
import platform

import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
import csv

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import keyboard
import re
import time
import threading


def kill_chrome_processes():
    if platform.system() == 'Linux':
        os.system('pkill -f chrome')
    elif platform.system() == 'Windows':
        os.system('taskkill /im chrome.exe /f')

# Configuração do serviço do WebDriver, driver google chrome
def setup_driver():
    # Encerrar processos existentes do Chrome
    kill_chrome_processes()
    
    service = Service(ChromeDriverManager().install())
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

def get_data_from_google_sheet(url_data, driver):
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
    style.configure("Treeview", rowheight=40)  # Aumentar a altura das linhas

    
    # Criação da barra de menu
    menu_bar = tk.Menu(root)

    # Menu Arquivo
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Planilha", command=spreadsheet)
    # file_menu.add_separator()
    file_menu.add_command(label="Udemy", command=udemy)
    menu_bar.add_cascade(label="Abrir", menu=file_menu)

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

     # Criando uma ListView com scroll vertical
    tree = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"), show="headings")
    tree.heading("col1", text="Index")
    tree.heading("col2", text="Cursos")
    tree.heading("col3", text="URL")
    tree.heading("col4", text="Categorias")
    tree.heading("col5", text="Plataforma")
    tree.heading("col6", text="URL Notion")
    tree.heading("col7", text="Coluna 7")
    tree.pack(fill="both", expand=True)
    
    # Lista para armazenar todas as linhas do CSV
    all_rows = []
    # Conjunto para armazenar valores únicos da coluna 4 (categorias dos cursos)
    unique_col4_values = set()

    # Itera sobre as linhas do CSV
    for row in csv_reader:
         # Inserir cada linha na ListView
        tree.insert("", "end", values=row)
        # salvar linhas do csv na var/lista all_rows 
        all_rows.append(row)
        # salvar os valores da coluna 4 na lista unique_col4_values
        unique_col4_values.add(row[3])
        
    # Ajustando a largura das colunas
    for col in tree["columns"]:
        # Define largura mínima e colocar o conteúdo na esquerda(="w") ou centraliza conteúdo(CENTER)
        tree.column(col, width=1, minwidth=0, anchor="w")
        # Centraliza o texto do cabeçalho
        tree.heading(col, anchor="w")
    tree.column(0, width=100, minwidth=100, anchor="w")
    tree.column(1, width=800, minwidth=780, anchor="w")

    frame = tk.Frame(root)
    frame.pack(padx=5, pady=10)

    # Dropdown para filtrar por valores da coluna 4
    col4_filter_label = tk.Label(frame, text="Filtrar por Categoria:")
    col4_filter_label.grid(row=0, column=0, padx=(0, 10), sticky="w", pady=10)

    col4_values = sorted(list(unique_col4_values))
    col4_filter_var = tk.StringVar(root)
    col4_filter_var.set("Todos") # Define o valor padrão como "Todos"
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
        else:
            # Filtra as linhas com base no valor selecionado na coluna 4
            filtered_rows = [row for row in all_rows if row[3] == selected_value]
            for row in filtered_rows:
                tree.insert("", "end", values=row)
    # Liga o evento de seleção do combobox
    col4_filter_dropdown.bind("<<ComboboxSelected>>", filter_data_with_combobox)

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
    # Define o evento de duplo clique na ListView
    tree.bind("<Double-1>", on_item_click)
    
    # Iniciar o loop principal da GUI
    root.mainloop()

def pause_and_play_video(driver):
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
    js_fast_forward = '''
    var video = document.getElementsByTagName('video')[0];
    function skip(value) {
        video.currentTime += value;
    }
    skip(3);
    '''
    driver.execute_script(js_fast_forward)
def teste(driver):
    js_test = '''
alert('teste')
    '''
    driver.execute_script(js_test)

def rewind_video(driver):
    js_rewind_video = '''
    var video = document.getElementsByTagName('video')[0];
    function rewind(value) {
        video.currentTime -= value;
    }
    rewind(3);
    '''
    driver.execute_script(js_rewind_video)
    
def next_video(driver):
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
    keyboard.add_hotkey('shift+l', lambda: pause_and_play_video(driver))
    keyboard.add_hotkey('shift+x', lambda: teste(driver))
    keyboard.add_hotkey('shift+=', lambda: increase_video_speed(driver))
    keyboard.add_hotkey('shift+-', lambda: decrease_video_speed(driver))
    keyboard.add_hotkey('shift+left', lambda: rewind_video(driver))
    keyboard.add_hotkey('shift+right', lambda: fast_forward_video(driver))
    keyboard.add_hotkey('shift+end', lambda: back_video(driver))
    keyboard.add_hotkey('shift+home', lambda: next_video(driver))
    # keyboard.add_hotkey('shift+end', lambda: driver.execute_script("document.querySelector('#go-to-next-item')?.click();"))
    # keyboard.add_hotkey('shift+home', lambda: driver.execute_script("document.querySelector('#go-to-previous-item')?.click();"))
    keyboard.add_hotkey('shift+k', lambda: toggle_video_subtitles(driver))

    keyboard.wait('ctrl+shift+esc')

def main():
    driver = setup_driver()
    # URL da planilha do Google Sheets
    url_data = "https://docs.google.com/spreadsheets/d/1Fg4cP6VEjQ5Ke8LCTSo88dUdZlc1az2RpBC6Bu6YuSw/gviz/tq?tqx=out:csv&range=A2:G80&sheet=Cursos"

    # Inicie a GUI do Tkinter em uma thread separada
    gui_thread = threading.Thread(target=get_data_from_google_sheet, args=(url_data, driver))
    gui_thread.start()

    # Inicie as hotkeys do tecladoX
    start_keyboard_shortcuts(driver)

if __name__ == "__main__":
    main()
