import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Dados de exemplo para preencher o Treeview
dados = [
    ("João", 30, "joao@email.com"),
    ("Maria", 25, "maria@email.com"),
    ("Pedro", 35, "pedro@email.com"),
    ("Ana", 28, "ana@email.com")
]

# Função para popular o Treeview com os dados
def popular_treeview(tree):
    for item in dados:
        tree.insert("", "end", values=item)

# Criar a janela principal
janela = tk.Tk()
janela.title("Exemplo de Treeview em Python")
janela.geometry("400x300")

# Criar o Treeview com colunas
tree = ttk.Treeview(janela, columns=("Nome", "Idade", "Email"), show="headings")

# Configurar cabeçalhos das colunas
tree.heading("Nome", text="Nome")
tree.heading("Idade", text="Idade")
tree.heading("Email", text="Email")

# Popular o Treeview com os dados
popular_treeview(tree)

# Ajustar largura das colunas
tree.column("Nome", width=100)
tree.column("Idade", width=50)
tree.column("Email", width=150)

# Posicionar o Treeview na janela
tree.pack(pady=20, padx=10)

# Executar o loop principal da janela
janela.mainloop()



#### GUI COM BOTÃO SIMPLES

def mostrar_mensagem():
    messagebox.showinfo("Mensagem", "Olá! Esta é uma GUI simples criada com tkinter.")

# Criar a janela principal
janela = tk.Tk()
janela.title("Minha GUI em Python")
janela.geometry("300x200")  # Definir o tamanho inicial da janela

# Criar um botão
botao = tk.Button(janela, text="Clique Aqui", command=mostrar_mensagem)
botao.pack(pady=20)  # Adicionar espaço ao redor do botão

# Executar o loop principal da janela
janela.mainloop()
