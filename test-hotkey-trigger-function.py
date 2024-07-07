import keyboard

0

# Função para associar a hotkey
def associar_hotkey():
    keyboard.add_hotkey('ctrl+i', minha_funcao)

# Associar a hotkey quando o script é executado
associar_hotkey()

# Mantém o script em execução para capturar a hotkey
keyboard.wait('esc')  # Aguarda pressionar ESC para sair