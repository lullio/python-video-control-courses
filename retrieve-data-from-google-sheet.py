import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
import csv

import tkinter as tk
from tkinter import ttk

import keyboard
import re
import time
import threading

# Configuração do serviço do WebDriver
def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--user-data-dir=C:/Users/Felipe/AppData/Local/Google/Chrome/User Data")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def get_data_from_google_sheet(url_data, driver):
    try:
        response = requests.get(url_data)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
    except requests.RequestException as e:
        print(f"Erro ao obter dados da planilha: {e}")
        return None

    csv_data = response.text
    csv_reader = csv.reader(csv_data.splitlines())

    root = tk.Tk()
    root.title("Gerenciador de Cursos - Felipe")

    tree = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"), show="headings")
    tree.heading("col1", text="Index")
    tree.heading("col2", text="Cursos")
    tree.heading("col3", text="URL")
    tree.heading("col4", text="Categorias")
    tree.heading("col5", text="Plataforma")
    tree.heading("col6", text="URL Notion")
    tree.heading("col7", text="Coluna 7")
    tree.pack(fill="both", expand=True)

    all_rows = []
    unique_col4_values = set()

    for row in csv_reader:
        tree.insert("", "end", values=row)
        all_rows.append(row)
        unique_col4_values.add(row[3])

    for col in tree["columns"]:
        tree.column(col, width=1, minwidth=1, anchor="w")
        tree.heading(col, anchor="w")
    tree.column(1, width=400, minwidth=400, anchor="w")

    frame = tk.Frame(root)
    frame.pack(padx=5, pady=10)

    col4_filter_label = tk.Label(frame, text="Filtrar por Categoria:")
    col4_filter_label.grid(row=0, column=0, padx=(0, 10), sticky="w", pady=10)

    col4_values = sorted(list(unique_col4_values))
    col4_filter_var = tk.StringVar(root)
    col4_filter_var.set("Todos")
    col4_filter_dropdown = ttk.Combobox(frame, textvariable=col4_filter_var, values=["Todos"] + col4_values, state="readonly", width=27)
    col4_filter_dropdown.grid(row=0, column=1, sticky="w")

    search_label = tk.Label(frame, text="Pesquisar:")
    search_label.grid(row=1, column=0, padx=(0, 10), sticky="w")

    search_var = tk.StringVar()
    search_entry = tk.Entry(frame, textvariable=search_var, width=30)
    search_entry.grid(row=1, column=1, sticky="we", padx=(0, 10))

    def filter_data_with_combobox(event=None):
        selected_value = col4_filter_var.get()
        tree.delete(*tree.get_children())
        if selected_value == "Todos":
            for row in all_rows:
                tree.insert("", "end", values=row)
        else:
            filtered_rows = [row for row in all_rows if row[3] == selected_value]
            for row in filtered_rows:
                tree.insert("", "end", values=row)

    col4_filter_dropdown.bind("<<ComboboxSelected>>", filter_data_with_combobox)

    def filter_data_with_search(event=None):
        query = search_var.get()
        tree.delete(*tree.get_children())
        try:
            regex = re.compile(query, re.IGNORECASE)
            for row in all_rows:
                if any(regex.search(str(value)) for value in row):
                    tree.insert("", "end", values=row)
        except re.error:
            pass

    search_var.trace_add("write", lambda *args: filter_data_with_search())

    def on_item_click(event):
        item = tree.selection()[0]
        if item:
            values = tree.item(item, "values")
            driver.get(values[2])
            webbrowser.open(values[5])

    tree.bind("<Double-1>", on_item_click)

    root.mainloop()

def pause_and_play_video(driver):
    js_play_video = '''
    var video = document.querySelectorAll('video')[0];
    if(document.querySelectorAll('video')[0]){
        document.querySelectorAll('video')[0].onplay = (e) => {
            e.target.playbackRate = localStorage.getItem('videoSpeed');
        }
    }
    if(video.paused){
        video.play();
    } else {
        video.pause();
    }
    '''
    driver.execute_script(js_play_video)

def change_video_speed(driver, increase=True):
    js_change_speed = '''
    var video = document.getElementsByTagName('video')[0];
    function speed(value) {
        video.playbackRate += value;
    }
    if({}) {{
        speed(0.25);
    }} else {{
        speed(-0.25);
    }}
    localStorage.setItem('videoSpeed', video.playbackRate);
    '''.format("true" if increase else "false")
    driver.execute_script(js_change_speed)

def fast_forward_video(driver):
    js_fast_forward = '''
    var video = document.getElementsByTagName('video')[0];
    function skip(value) {
        video.currentTime += value;
    }
    skip(3);
    '''
    driver.execute_script(js_fast_forward)

def rewind_video(driver):
    js_rewind_video = '''
    var video = document.getElementsByTagName('video')[0];
    function rewind(value) {
        video.currentTime -= value;
    }
    rewind(3);
    '''
    driver.execute_script(js_rewind_video)

def toggle_video_subtitles(driver):
    js_toggle_subtitles = '''
    var subtitlesButton = document.querySelector('[aria-label="Legendas"], [aria-label="Subtitles"]');
    subtitlesButton.click();
    var options = document.querySelectorAll('ul[aria-label="Legendas"] li, ul[aria-label="Subtitles"] li');
    options.forEach(option => {
        if(option.textContent.includes('Ingl') || option.textContent.includes('English')) {
            option.click();
        } else if(option.textContent.includes('Deslig') || option.textContent.includes('Off')) {
            option.click();
        }
    });
    '''
    driver.execute_script(js_toggle_subtitles)

def start_keyboard_shortcuts(driver):
    keyboard.add_hotkey('alt+l', lambda: pause_and_play_video(driver))
    keyboard.add_hotkey('alt+=', lambda: change_video_speed(driver, increase=True))
    keyboard.add_hotkey('alt+-', lambda: change_video_speed(driver, increase=False))
    keyboard.add_hotkey('alt+left', lambda: rewind_video(driver))
    keyboard.add_hotkey('alt+right', lambda: fast_forward_video(driver))
    keyboard.add_hotkey('alt+end', lambda: driver.execute_script("document.querySelector('#go-to-next-item').click();"))
    keyboard.add_hotkey('alt+home', lambda: driver.execute_script("document.querySelector('#go-to-previous-item').click();"))
    keyboard.add_hotkey('alt+k', lambda: toggle_video_subtitles(driver))

    keyboard.wait('esc')

def main():
    driver = setup_driver()
    url_data = "https://docs.google.com/spreadsheets/d/1Fg4cP6VEjQ5Ke8LCTSo88dUdZlc1az2RpBC6Bu6YuSw/gviz/tq?tqx=out:csv&range=A2:G80&sheet=Cursos"

    # Inicie a GUI do Tkinter em uma thread separada
    gui_thread = threading.Thread(target=get_data_from_google_sheet, args=(url_data, driver))
    gui_thread.start()

    # Inicie as hotkeys do teclado
    start_keyboard_shortcuts(driver)

if __name__ == "__main__":
    main()
