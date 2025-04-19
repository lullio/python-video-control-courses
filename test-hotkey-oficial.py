import keyboard

keyboard.add_hotkey('shift+x', lambda: print("ALT+X funcionando!"))
print("Teste: Pressione ALT+X")
keyboard.wait('esc')  # Pressione ESC para sair