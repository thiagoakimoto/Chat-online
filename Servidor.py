import socket
import threading

# Dicionário para armazenar sockets e nomes
lista_clientes = {}

# Fnc para recebimento de mensagens
def recebe_dados(sock_cliente, endereco):
    nome = sock_cliente.recv(50).decode()
    print(f"Conexão bem sucedida com {nome} via endereço: {endereco}")
    lista_clientes[sock_cliente] = nome  # Armazena o usuário
    # Notifica todos a entrada do novo usuário
    broadcast(f"{nome} entrou no chat.", nome)

    while True:
        try:
            mensagem = sock_cliente.recv(1024).decode()
            if mensagem:
                print(f"{nome} >> {mensagem}")

                if mensagem.startswith("/"):
                    try:
                        nome_destino, msg_real = mensagem[1:].split(" ", 1)
                        unicast(f"{nome} (privado): {msg_real}", nome_destino)
                    except ValueError:
                        sock_cliente.sendall("Formato inválido. Use: /nome_destinatario mensagem".encode())
                else:
                    broadcast(f"{nome}: {mensagem}", nome)
        except:
            print(f"{nome} foi desconectado...")
            remover_cliente(sock_cliente)
            break

# Fnc para envio de broadcast 
def broadcast(mensagem, nome):
    for cliente_socket, cliente_nome in lista_clientes.items():
        if cliente_nome != nome:  # Evita enviar a mensagem ao próprio remetente
            try:
                cliente_socket.sendall(mensagem.encode())
            except Exception as e:
                print(f"Erro ao enviar para {cliente_nome}: {e}")
                remover_cliente(cliente_socket)  # Remove o cliente em caso de erro ao enviar

# fnc unicast que manda mensaagem privada
def unicast(mensagem, nome_destino):
    for cliente_socket, cliente_nome in lista_clientes.items():
        if cliente_nome == nome_destino:
            try:
                cliente_socket.sendall(mensagem.encode())
                return
            except Exception as e:
                print(f"Erro ao enviar mensagem unicast para {nome_destino}: {e}")
                remover_cliente(cliente_socket)  # remove usuario
    print(f"Usuário {nome_destino} não encontrado para mensagem privada.")

# Fnc q remove usuário 
def remover_cliente(sock_cliente):
    nome = lista_clientes.get(sock_cliente)
    if nome:
        print(f"Removendo {nome} da lista de clientes.")
        del lista_clientes[sock_cliente]  # remove o usuário
        sock_cliente.close()  # Fecha a conexão
        broadcast(f"{nome} saiu do chat.", nome)  # Notificação para outros usuários

# config de host e porta
HOST = '127.0.0.1'
PORTA = 9999

# Cria o socket do servidor
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# link do ip e porta
sock_server.bind((HOST, PORTA))

# Abre o servidor
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

# O sv tem que aceitar as diversas conexões
while True:
    sock_conn, ender = sock_server.accept()
    print(f"Cliente conectado: {ender}")
    
    # Cria uma thread para lidar com o cliente conectado
    thread_cliente = threading.Thread(target=recebe_dados, args=(sock_conn, ender))
    thread_cliente.daemon = True  # Utilizamos a thread que impede o encerramento do programa
    thread_cliente.start()
