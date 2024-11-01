import socket 
import threading
#função que recebe mensagem do cliente
def  recebe_dados (sock_cliente, endereco):
    #receber o nome (máx 50 carac) decotes() bytes -> str
    nome = sock_cliente.recv(50).decode()
    print(f"Conexão bem sucedida com {nome} via endereço: {endereco}")
    while True:
            try: 
                mensagem = sock_cliente.recv(1024).decode()
                print(f"Cliente >> {mensagem}")
            except:
                 print("Erro ao receber mensagem... fechamos")
                 sock_cliente.close()
                 return
#implementar broadcast      
def broadcast(lista_clientes):
     pass
#implementar unicast
def unicast(cliente): 
     pass
#implementar remoção do cliente quando ele sair do chat
def remover(cliente):
     pass



#endereço utilizado para o servidor
HOST = '127.0.0.1'
PORTA = 9999

lista_clietes = []
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#fazemos o bind  - > Link do ip:porta
sock_server.bind((HOST, PORTA))

#abrimos o servidor para o nome de escuta

sock_server.listen()
print(f'O servidor {HOST}: {PORTA} está aguardando conexões...')


#O servidor deve aceitar uma conexão solicitada pelo cliente
#Criar um loop para o servidor acerar várias conexões
while True:
    sock_conn, ender = sock_server.accept()
    #Conexão com sucesso, vamos receber dados
    #CRIamos um loop para recebimento das mensagens do cliente
    #Criamos uma thread para a função recebe_dados(sock_conn, ender)
    #sock_con é o socket de conexão vindo do cliente
    thread_cliente = threading.Thread(target=recebe_dados, args=[sock_conn,ender])
    thread_cliente.start()




