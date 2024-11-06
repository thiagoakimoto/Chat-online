import socket
import threading
#Função para recebimento de mensagem do cliente
def recebe_dados(sock_cliente, endereco):
    # Receber o nome do cliente (máximo 50 caracteres)
    nome = sock_cliente.recv(50).decode()
    print(f"Conexão bem sucedida com {nome} via endereço: {endereco}")
    lista_clientes[sock_cliente] = nome  # Armazena o cliente pelo socket

    while True:
        try:
            mensagem = sock_cliente.recv(1024).decode()
            if mensagem:
                print(f"{nome} >> {mensagem}")

                # Mensagens privadas (unicast) usando comando "/"
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
# Função para envio de mensagem a todos os clientes conectados (broadcast)
def broadcast(mensagem, nome):
    for cliente_socket, cliente_nome in lista_clientes.items():
        if cliente_nome != nome:  # Evita enviar a mensagem ao próprio remetente
            try:
                cliente_socket.sendall(mensagem.encode())
            except Exception as e:
                print(f"Erro ao enviar para {cliente_nome}: {e}")
#implementar unicast
def unicast(mensagem, nome_destino):
    for cliente_socket, cliente_nome in lista_clientes.items():
        if cliente_nome == nome_destino:
            try:
                cliente_socket.sendall(mensagem.encode())
                return
            except Exception as e:
                print(f"Erro ao enviar mensagem unicast para {nome_destino}: {e}")
    print(f"Usuário {nome_destino} não encontrado para mensagem privada.")

    
#implementar remoção do cliente quando ele sair do chat
def remover(mensagem, lista_cliente):
    pass
#Endereço que será utilizado para o servidor
HOST = '127.0.0.1'
PORTA = 9999

lista_clientes = {}

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



#fazemos o bind -> LINK do IP:PORTA
sock_server.bind((HOST,PORTA))

#abrimos o servidor para o mode de escuta
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

#O servidor deve aceitar uma conexão solicitada pelo cliente
#Vamos criar um loop para o servidor acertar várias conexões
while True:
    sock_conn, ender = sock_server.accept()
    #Conexão com sucesso, vamos receber dados
    #Criamos um loop para recebimento das mensagens do cliente
    #Criamos uma thread para a função recebe_dados(sock_conn, ender)
    #sock_conn é o socket de conexão vindo do cliente
    thread_cliente = threading.Thread(target=recebe_dados, args=[sock_conn, ender])
    thread_cliente.start()
