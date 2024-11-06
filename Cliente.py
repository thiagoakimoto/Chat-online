import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# IP e PORTA do servidor que queremos nos conectar
HOST = '127.0.0.1'
PORTA = 9999
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Fnc da interface
def interface():
    janela = tk.Tk()
    janela.title("Chat Prof Gui")
    janela.geometry("400x500")

    texto_chat = scrolledtext.ScrolledText(janela, width=40, height=10)
    texto_chat.pack(pady=10)  # Corrigido de `text_chat.pack` para `texto_chat.pack`

    entrada_mensagem = tk.Entry(janela, width=50)
    entrada_mensagem.pack(pady=5)
    entrada_mensagem.bind("<Return>", lambda event: enviar_mensagem(entrada_mensagem.get()))

    enviar_button = tk.Button(janela, text="Enviar", command=lambda: enviar_mensagem(entrada_mensagem.get()))
    enviar_button.pack(pady=5)
    return janela, texto_chat, entrada_mensagem

# Fnc que conecta ao servidor
def conectar_server():
    global socket_cliente
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Corrigido de `sock` para `socket`
    socket_cliente.connect((HOST, PORTA))

    nome = input("Insira seu nome para logar no chat: ")
    socket_cliente.sendall(nome.encode())
    exibir_mensagem(f"Você entrou no chat como {nome}.")

    # Thread para receber mnsg do sv
    thread = threading.Thread(target=receber_mensagem)
    thread.start()

# Fnc para enviar mensagens
def enviar_mensagem(mensagem):
    if mensagem:
        entrada_mensagem.delete(0, tk.END)  # Limpa o campo de entrada
        socket_cliente.sendall(mensagem.encode())

        # Corrigido a indentação para evitar erro
        if mensagem.startswith("/"):
            exibir_mensagem(f"Você (privado): {mensagem}")
        else:
            exibir_mensagem(f"Você: {mensagem}")

# Função para receber mensagens do servidor
def receber_mensagem():
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()
            exibir_mensagem(mensagem)
        except:
            print("Erro ao receber mensagem... desconectando")
            socket_cliente.close()
            break

# Função auxiliar para exibir mensagens na interface
def exibir_mensagem(mensagem):
    texto_chat.config(state=tk.NORMAL)
    texto_chat.insert(tk.END, mensagem + '\n')
    texto_chat.config(state=tk.DISABLED)

# Inicializa a interface
janela, texto_chat, entrada_mensagem = interface()
conectar_server()
janela.mainloop()
