import threading


def loop_infinito():

    while True:
        texto = input(' ')
        if texto == 'b ':
            break

n=10000
def loop_finito(n):
    while  n > 0:
        print(f'a{n}')
        n = n - 1
    
n=100000
#Vamos criar threads que executaram em funções locais diferentes de memória

thread1 = threading.Thread(target=loop_infinito)
thread2 = threading.Thread(target=loop_finito, args=[n])

thread1.start()
thread2.start()



print('Saindo do loop...')


