import socket 

#IP e PORTA do servidor que queremos nos conectar
HOST = '127.0.0.1'
PORTA = 9999
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#cliente solicita conexão
socket_cliente.connect((HOST, PORTA))
print(5*"-" + "CHAT INICIADO" + 5*"-")
#INformar o nome ao servidor
nome = input("INforme seu nome para entrar no chat:")
socket_cliente.sendall(nome.encode())

#loop de envio de dados
while True:
    mensagem = input('')
    #Para enviar damos o encode() para transformar em bytes str -> bytes
    socket_cliente.sendall(mensagem.encode())