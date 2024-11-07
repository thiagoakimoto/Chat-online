import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# IP e PORTA do servidor que queremos nos conectar
HOST = '127.0.0.1'# IP local (localhost), utilizado para testes no mesmo computador 
PORTA = 9999 # Porta do servidor à qual o cliente se conecta
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Fnc da interface gráfica do servidor
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

# Fnc que conecta ao servidor -- socket permite a comunicação entre diferentes computadores por meio de redes, pode ser feito por tcp e udp 
def conectar_server():
    global socket_cliente # Declara socket_cliente como global para ser acessado em outras funções
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Corrigido de `sock` para `socket`
    socket_cliente.connect((HOST, PORTA))# Conecta ao servidor com IP e porta especificados

    nome = input("Insira seu nome para logar no chat: ")
    socket_cliente.sendall(nome.encode()) # Envia o nome codificado para o servidor
    exibir_mensagem(f"Você entrou no chat como {nome}.")

    # Thread para receber mnsg do sv
    thread = threading.Thread(target=receber_mensagem)
    thread.start()

# Fnc para enviar mensagens ao servidor 
def enviar_mensagem(mensagem):
    if mensagem: # Verifica se a mensagem não está vazia
        entrada_mensagem.delete(0, tk.END)  # Limpa o campo de entrada
        socket_cliente.sendall(mensagem.encode())# Envia a mensagem codificada ao servidor

        # Corrigido a indentação para evitar erro
        if mensagem.startswith("/"):
            exibir_mensagem(f"Você (privado): {mensagem}")
        else:
            exibir_mensagem(f"Você: {mensagem}")

# Função para receber mensagens do servidor
def receber_mensagem():
    while True:
        try:
             # Recebe a mensagem do servidor e a decodifica
            mensagem = socket_cliente.recv(1024).decode()
            exibir_mensagem(mensagem)
        except:
             # Em caso de erro (ex.: servidor desconectado), fecha o socket e sai do loop
            print("Erro ao receber mensagem... desconectando")
            socket_cliente.close()
            break

# Função auxiliar para exibir mensagens na interface
def exibir_mensagem(mensagem):
    texto_chat.config(state=tk.NORMAL) # Permite edição do campo de texto
    texto_chat.insert(tk.END, mensagem + '\n')# Insere a nova mensagem ao final do campo de texto
    texto_chat.config(state=tk.DISABLED)  # Desabilita edição do campo de texto após inserção

# Inicializa a interface
janela, texto_chat, entrada_mensagem = interface() # Configura a interface e guarda os elementos principais
conectar_server()# Conecta o cliente ao servidor
janela.mainloop()# Inicia o loop principal da interface gráfica
