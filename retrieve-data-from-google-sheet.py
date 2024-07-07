import webbrowser # para abrir o browser, bem mais simples q selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager

import requests
import csv

import tkinter as tk
from tkinter import ttk

import keyboard
import re

# Configuração do serviço do WebDriver
service = Service(ChromeDriverManager().install())
# Configuração do navegador Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Abrir navegador maximizado
options.add_argument("--user-data-dir=C:/Users/Felipe/AppData/Local/Google/Chrome/User Data")  # Diretório do perfil padrão
options.add_argument("--profile-directory=Default")  # Diretório do perfil padrão
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

# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 

# Inicialização do driver do Chrome
driver = webdriver.Chrome(service=service, options=options)

# Changing the property of the navigator value for webdriver to undefined 
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

# Encerrar o navegador
#driver.quit()

def get_data_from_google_sheet(url_data):
    # Realiza uma requisição GET para obter o conteúdo da planilha
    response = requests.get(url_data)
    
    # Verifica se a requisição foi bem-sucedida (código 200)
    if response.status_code == 200:
         # Lê o conteúdo CSV retornado pela API do Google Sheets
        csv_data = response.text
        
         # Utiliza o módulo csv para ler os dados CSV
        csv_reader = csv.reader(csv_data.splitlines())
        
        # Criando a janela principal da aplicação
        root = tk.Tk()
        root.title("Gerenciador de Cursos - Felipe")
        
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
            all_rows.append(row) # salvar linhas do csv
            unique_col4_values.add(row[3])  # Adiciona valor da coluna 4 aos valores únicos
            
        # Ajustando a largura das colunas
        for col in tree["columns"]:
            tree.column(col, width=1, minwidth=1, anchor="w")  # Define largura mínima e colocar o conteúdo na esquerda(="w") ou centraliza conteúdo(CENTER)
            tree.heading(col, anchor="w")  # Centraliza o texto do cabeçalho
        tree.column(1, width=400, minwidth=400, anchor="w" )
        
         # Dropdown para filtrar por valores da coluna 4
         
        # Frame para conter os widgets (Label e Combobox). Isso ajuda na organização e posicionamento dos elementos na interface.
        frame = tk.Frame(root)
        frame.pack(padx=5, pady=10)
        
        # PRIMEIRA LINHA
        # Texto à esquerda (Label)
        col4_filter_label = tk.Label(frame, text="Filtrar por Categoria:")
        col4_filter_label.grid(row=0, column=0, padx=(0, 10), sticky="w", pady=10)  # Alinha à esquerda com padding à direita
        # col4_filter_label.pack(side=tk.LEFT, padx=(0, 10))  # Alinha à esquerda com padding à direita
        
        # Combobox à direita
        col4_values = sorted(list(unique_col4_values))
        col4_filter_var = tk.StringVar(root)
        col4_filter_var.set("Todos")  # Define o valor padrão como "Todos"
        col4_filter_dropdown = ttk.Combobox(frame, textvariable=col4_filter_var, values=["Todos"] + col4_values, state="readonly", width=27)
        col4_filter_dropdown.grid(row=0, column=1, sticky="w")  # Alinha à esquerda
        # col4_filter_dropdown.pack(side=tk.LEFT)  # Alinha à esquerda
        
        
        # SEGUNDA LINHA
        # Label do campo de pesquisa
        search_label = tk.Label(frame, text="Pesquisar:")
        search_label.grid(row=1, column=0, padx=(0, 10), sticky="w")  # Alinha à esquerda com padding à direita
        
        # Campo de pesquisa com regex
        search_var = tk.StringVar()
        search_entry = tk.Entry(frame, textvariable=search_var, width=30)
        search_entry.grid(row=1, column=1, sticky="we", padx=(0, 10))  # Preenche horizontalmente e alinha à esquerda
        #search_entry.pack(pady=10)
        # Função para filtrar os dados da Treeview com base no valor selecionado no dropdown
        def filter_data_with_combobox(event=None):
            selected_value = col4_filter_var.get()
            
            if selected_value == "Todos":
                # Mostra todas as linhas se "Todos" estiver selecionado
                tree.delete(*tree.get_children())
                for row in all_rows:
                    tree.insert("", "end", values=row)
            else:
                # Filtra as linhas com base no valor selecionado na coluna 4
                filtered_rows = [row for row in all_rows if row[3] == selected_value]
                tree.delete(*tree.get_children())
                for row in filtered_rows:
                    tree.insert("", "end", values=row)
        
        col4_filter_dropdown.bind("<<ComboboxSelected>>", filter_data_with_combobox)  # Liga o evento de seleção do combobox
        

        
        def filter_data_with_search(event=None):
            query = search_var.get()
            tree.delete(*tree.get_children())  # Limpa a Treeview antes de aplicar o filtro
            
            try:
                regex = re.compile(query, re.IGNORECASE)  # Regex case insensitive
                for row in all_rows:
                    if any(regex.search(str(value)) for value in row):
                        tree.insert("", "end", values=row)
            except re.error:
                pass
        
        search_var.trace_add("write", lambda *args: filter_data_with_search())  # Adiciona rastreador para atualizar ao digitar
        
        
        # Função para lidar com o clique duplo na ListView
        def on_item_click(event):
            item = tree.selection()[0]
            if item:
                # Obtém os valores da linha clicada
                values = tree.item(item, "values")
                # Abre o navegador com o link da coluna 3 (índice 2)
                driver.get(values[2]) # Coluna 3 = url do curso usando selenium pois quero abrir no meu perfil Felipe do Chrome
                webbrowser.open(values[5]) # Coluna 6 = url do notion
        
        tree.bind("<Double-1>", on_item_click)  # Define o evento de duplo clique na ListView
        
        # Iniciar o loop principal da GUI
        root.mainloop()
        return csv_data
    else:
        print(f"Erro ao obter dados da planilha. Código de status: {response.status_code}")
        return None 
    
# DEFINIR AS HOTKEYS
 
def pause_and_play_video():
    # Injetar e executar JavaScript no contexto da página
    js_play_video = '''
{
var video = document.querySelectorAll('video')[0];
/*
FIX TOP QUE ARRUMEI PARA NÃO RESETAR O playbackRate ao dar play no video
*/
if(document.querySelectorAll('video')[0]){
	document.querySelectorAll('video')[0].onplay = (e) => {
		e.target.playbackRate = localStorage.getItem('videoSpeed');
		console.log("playbackRate ajustado para: ", e.target.playbackRate)
	}
}
// TOGGLE PAUSAR / PlLAY
if(document.querySelectorAll('video')[0].paused){ // se tiver pausado, paused é um método js
	document.querySelectorAll('video')[0].play();
	console.log("play no video")
}else{
	// video?.playbackRate = localStorage.getItem('videoSpeed');
	document.querySelectorAll('video')[0].pause();
	// video?.defaultPlaybackRate = localStorage.getItem('videoSpeed');
	console.log("pause no video");
}
}
'''
    driver.execute_script(js_play_video) # executar javascript no console / chrome
def increase_video_speed():
    # Injetar e executar JavaScript no contexto da página
    js_increase_speed = '''
// capturar o video
{
var video = document.getElementsByTagName('video')[0];

// aumentar velocidade do video
function speed(value = 0.25) {
  video.playbackRate += value;
}
if(video.playbackRate <=4.0){ // para não dar erro, executar somente se a velocidade for menor ou igual a 4
  speed(); // executar função
  console.log("aumentei a velocidade: ", video.playbackRate);
  localStorage.setItem('videoSpeed', video.playbackRate);
}
}
'''
    driver.execute_script(js_increase_speed) # executar javascript no console / chrome
def decrease_video_speed():
    # Injetar e executar JavaScript no contexto da página
    js_decrease_speed = '''
// capturar o video

var video = document.getElementsByTagName('video')[0];

// diminuir velocidade do video
function speed(value = 0.25) {
  video.playbackRate -= value;
  video.defaultPlaybackRate -= value;
}
if(video.playbackRate >= 0.25){ // para não dar erro , só executar se a velocidade do video for maior ou igual a 0.25
  speed(); // executar função
  console.log("diminui a velocidade: ", video.playbackRate);
  localStorage.setItem('videoSpeed', video.playbackRate);
}
'''
    driver.execute_script(js_decrease_speed) # executar javascript no console / chrome
def fast_forward_video():
    # Injetar e executar JavaScript no contexto da página
    js_fast_forward = '''
// capturar o video
{
var video = document.getElementsByTagName('video')[0];

// avançar video, parametro com valor padrao de 3 segundos, caso nao passe um argumento na funcao
function skip(value = 3) {
  video.currentTime += value;
}
skip(); // executar função
}
'''
    driver.execute_script(js_fast_forward) # executar javascript no console / chrome
def rewind_video():
    # Injetar e executar JavaScript no contexto da página
    js_rewind_video = '''
// capturar o video
{
var video = document.getElementsByTagName('video')[0];

// voltar 3 segundos de video
function rewind(value = 3) {
  video.currentTime -= value;
}
rewind(); // executar função
}

'''
    driver.execute_script(js_rewind_video) # executar javascript no console / chrome
def rewind_video():
    # Injetar e executar JavaScript no contexto da página
    js_rewind_video = '''
// capturar o video
{
var video = document.getElementsByTagName('video')[0];

// voltar 3 segundos de video
function rewind(value = 3) {
  video.currentTime -= value;
}
rewind(); // executar função
}

'''
    driver.execute_script(js_rewind_video) # executar javascript no console / chrome
def toggle_video_subtitles():
    # Injetar e executar JavaScript no contexto da página
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
    driver.execute_script(js_toggle_subtitles) # executar javascript no console / chrome
def skip_video():
    # Injetar e executar JavaScript no contexto da página
    js_skip_video = '''
{
// capturar o video
{
var video = document.getElementsByTagName('video')[0];

var goNext = document.querySelectorAll('#go-to-next-item')[0];

// avançar pro próximo vídeo
goNext.click();

}
'''
    driver.execute_script(js_skip_video) # executar javascript no console / chrome
def previous_video():
    # Injetar e executar JavaScript no contexto da página
    js_previous_video = '''
    alert('HI')
// capturar o video
{
var video = document.getElementsByTagName('video')[0];

var goPrevious = document.querySelectorAll('#go-to-previous-item')[0];

// voltar pro video anterior
goPrevious.click();

}
'''
    driver.execute_script(js_previous_video) # executar javascript no console / chrome




# URL da planilha do Google Sheets
url_data = "https://docs.google.com/spreadsheets/d/1Fg4cP6VEjQ5Ke8LCTSo88dUdZlc1az2RpBC6Bu6YuSw/gviz/tq?tqx=out:csv&range=A2:G80&sheet=Cursos"

# Associar a hotkey quando o script é executado
# Chamada da função para obter os dados
planilha_data = get_data_from_google_sheet(url_data)
# Exibição dos dados (opcional)
print(planilha_data) 


# Associar as hotkeys
def associar_hotkeys():
    keyboard.add_hotkey('alt+l', pause_and_play_video)
    keyboard.add_hotkey('win+l', pause_and_play_video)
    keyboard.add_hotkey('alt+=', increase_video_speed)
    keyboard.add_hotkey('alt+-', decrease_video_speed)
    keyboard.add_hotkey('alt+left', rewind_video)
    keyboard.add_hotkey('alt+right', fast_forward_video)
    keyboard.add_hotkey('alt+end', skip_video)
    keyboard.add_hotkey('alt+home', previous_video)
    keyboard.add_hotkey('alt+k', toggle_video_subtitles)

# Associar a hotkey quando o script é executado
associar_hotkeys()

# Mantém o script em execução para capturar a hotkey
keyboard.wait('esc')  # Aguarda pressionar ESC para sair