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

# Inicialização do driver do Chrome
driver = webdriver.Chrome(service=service, options=options)
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
        root.title("Dados da Planilha")
        
        # Criando uma ListView com scroll vertical
        tree = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"), show="headings")
        tree.heading("col1", text="Index")
        tree.heading("col2", text="Curso")
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
        tree.column(1, width=300, minwidth=300, anchor="w" )
        
         # Dropdown para filtrar por valores da coluna 4
        col4_values = sorted(list(unique_col4_values))
        col4_filter_var = tk.StringVar(root)
        col4_filter_var.set("Todos")  # Define o valor padrão como "Todos"
        
        col4_filter_label = tk.Label(root, text="Filtrar por Coluna 4:")
        col4_filter_label.pack(pady=10)
        
        col4_filter_dropdown = ttk.Combobox(root, textvariable=col4_filter_var, values=["Todos"] + col4_values, state="readonly")
        col4_filter_dropdown.pack()
        
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
        
        # Campo de pesquisa com regex
        search_var = tk.StringVar()
        search_entry = tk.Entry(root, textvariable=search_var, width=30)
        search_entry.pack(pady=10)
        
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
 
def minha_funcao():
    # Injetar e executar JavaScript no contexto da página
    print("hello")
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
# Função para associar a hotkey
def associar_hotkey():
    keyboard.add_hotkey('ctrl+i', minha_funcao) 
 

# URL da planilha do Google Sheets
url_data = "https://docs.google.com/spreadsheets/d/1Fg4cP6VEjQ5Ke8LCTSo88dUdZlc1az2RpBC6Bu6YuSw/gviz/tq?tqx=out:csv&range=A2:G80&sheet=Cursos"

# Associar a hotkey quando o script é executado
associar_hotkey()
# Chamada da função para obter os dados
planilha_data = get_data_from_google_sheet(url_data)


# Exibição dos dados (opcional)
print(planilha_data)



