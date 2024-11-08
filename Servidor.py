import socket
import threading

# Dicionário para armazenar sockets e nomes dos clientes
lista_clientes = {}

def recebe_dados(sock_cliente, endereco):
    nome = sock_cliente.recv(50).decode()  # Recebe o nome do cliente e o decodifica
    print(f"Conexão bem sucedida com {nome} via endereço: {endereco}")
    lista_clientes[sock_cliente] = nome  # Armazena o usuário
    
    # Notifica todos a entrada do novo usuário
    broadcast(f"{nome} entrou no chat.", nome)
    
    # Loop para receber mensagens contínuas do cliente
    while True:
        try:
            # Recebe a mensagem do cliente e a decodifica
            mensagem = sock_cliente.recv(1024).decode()

            if mensagem == '#sair':
                remover_cliente(sock_cliente)
                break

            # Verifica se a mensagem não está vazia
            if mensagem:
                print(f"{nome} >> {mensagem}")
                
                # Verifica se a mensagem é privada (inicia com '/')
                if mensagem.startswith("/"):
                    try:
                        # Separa o nome do destinatário e a mensagem privada
                        nome_destino, msg_real = mensagem[1:].split(" ", 1)
                        # Envia a mensagem privada ao destinatário especificado
                        unicast(f"{nome} (privado): {msg_real}", nome_destino)
                    except ValueError:
                        # Caso a mensagem privada esteja em formato incorreto, notifica o usuário
                        sock_cliente.sendall("Formato inválido. Use: /nome_destinatario mensagem".encode())
                else:
                    # Se não for mensagem privada, envia para todos (broadcast)
                    broadcast(f"{nome}: {mensagem}", nome)
        except ConnectionResetError:
            # Notifica a todos que o cliente foi desconectado e o remove da lista
            print("exept rodando")
            broadcast(f"{nome} foi desconectado...", " ")  # Nome vazio para indicar que é uma notificação
            remover_cliente(sock_cliente)
            break
        


# # Função para enviar uma mensagem para todos os clientes (exceto o remetente) 
def broadcast(mensagem, nome):
    for cliente_socket, cliente_nome in lista_clientes.items():
        # Evita enviar a mensagem ao próprio remetente
        if cliente_nome != nome:  # Evita enviar a mensagem ao próprio remetente
            try:
                cliente_socket.sendall(mensagem.encode()) # Envia a mensagem para o cliente atual
            except Exception as e:
                 # Em caso de erro ao enviar a mensagem, remove o cliente da lista
                print(f"Erro ao enviar para {cliente_nome}: {e}")
                remover_cliente(cliente_socket)  # Remove o cliente em caso de erro ao enviar

#  Função unicast para enviar uma mensagem privada para um único cliente 
def unicast(mensagem, nome_destino):
    for cliente_socket, cliente_nome in lista_clientes.items():
        # Verifica se o nome do cliente corresponde ao destinatário
        if cliente_nome == nome_destino:
            try:
                cliente_socket.sendall(mensagem.encode()) # Envia a mensagem privada ao destinatário
                return
            except Exception as e:
                print(f"Erro ao enviar mensagem unicast para {nome_destino}: {e}") # Em caso de erro ao enviar a mensagem privada, remove o cliente
                remover_cliente(cliente_socket) 
                 # Caso o destinatário não seja encontrado, notifica no servidor
    print(f"Usuário {nome_destino} não encontrado para mensagem privada.")


def remover_cliente(sock_cliente):
    nome = lista_clientes.get(sock_cliente) # Obtém o nome do cliente a partir do socket
    if nome:
        print(f"Removendo {nome} da lista de clientes.")

        del lista_clientes[sock_cliente]  # remove o usuário
        sock_cliente.close()  # Fecha a conexão
        broadcast(f"{nome} saiu do chat.", nome)  # Notificação para outros usuários que saiu do chat



# config de host e porta
HOST = '25.15.75.111'# IP local para testes (localhost)
PORTA = 9999  # Porta do servidor para conexão dos clientes

# # Cria o socket do servidor para aceitar conexões TCP (permite que dispostivos e programas troquem mensagens em uma rede) 
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula o socket à porta e IP configurados
sock_server.bind((HOST, PORTA))

# Abre o servidor
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

# O sv tem que aceitar as diversas conexões
while True:
    # Aceita uma nova conexão de cliente
    sock_conn, ender = sock_server.accept()
    print(f"Cliente conectado: {ender}")
    
    # # Cria uma thread para lidar com o cliente conectado, permitindo múltiplas conexões
    thread_cliente = threading.Thread(target=recebe_dados, args=(sock_conn, ender))
    thread_cliente.daemon = True  # Utilizamos a thread que impede o encerramento do programa
    thread_cliente.start() # Inicia a thread para receber mensagens do cliente
