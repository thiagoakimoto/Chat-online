import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

#IP e PORTA do servidor que queremos nos conectar
HOST = '127.0.0.1'
PORTA = 9999
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Fnc da interface
def interface():
    janela = tk.Tk()
    janela.title("Chat Prof Gui")
    janela.geometry("300x400")
    texto_chat = scrolledtext.ScrolledText(janela, width=40, height=10)
    text_chat.pack(pady=10)
    entrada_mensagem = tk.Entry(janela, width=50)
    entrada_mensagem.pack(pady=5)
    entrada_mensagem.bind("<Return>", lambda event: enviar_mensagem(entrada_mensagem.get()))
    enviar_button = tk.Button(janela, text="Enviar", command=lambda: enviar_mensagem)
    enviar_button.pack(pady=5)
    return janela, texto_chat, entrada_mensagem

#Fnc que conecta
def conectar_server():
    global socket_cliente
    socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    socket_cliente.connect((HOST, PORTA))
    nome = input("Insira seu nome para logar no chat: ")
    socket_cliente.sendall(nome.encode())
    exibir_mensagem(f"Você entrou no chat como {nome}.")
    thread = threading.Thread(target=receber_mensagem)
    thread.start()

def enviar_mensagem():
   if mensagem:
       entrada_mensagem.delete(0, tk.END)
       socket_cliente.sendall(mensagem.encode())
       if mensagem.startswith("/"):
           exibir_mensagem(f"Você (privado): {mensagem}")
        else:
           exibir_mensagem(f"Você: {mensagem}")


def receber_mensagem():
      while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()
            exibir_mensagem(mensagem)
        except:
            print("Erro ao receber mensagem...desconectando")
            socket_cliente.close()
            break

#cliente solicita conexão

#Vamos informar o nome
nome = input("Informe seu nome para entrar no chat: ")
socket_cliente.sendall(nome.encode())

#Loop de envio de dados
while True:
    mensagem = input('')
#Para enviar damos o encode() para transformar em bytes str -> bytes
socket_cliente.sendall(mensagem.encode())
