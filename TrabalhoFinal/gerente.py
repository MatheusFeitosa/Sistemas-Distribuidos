#imports
import socket
import select
import sys
import subprocess
import os
import time

HOST = '' 
PORT = 4988

entradas = [sys.stdin]
conexoes = {}

N = 10

nosfilhos = []
processos = []
ativos = []
portas = []

def criarNos():
    for i in range(N):
        PORTA = PORT + i + 1
        PORTA = str(PORTA)
        criarNo(i, N, PORTA)

#Referencia https://stackabuse.com/executing-shell-commands-with-python/
def criarNo(id, tamanho, PORTA):
    processo = subprocess.Popen(["python3", "no.py", str(id), str(PORTA), str(tamanho)])
    processos.append(processo)
    time.sleep(1)
    portas.append(PORTA)
    conectarInicio(PORTA)

def conectarInicio(PORTA):
    sockInicio = socket.socket()
    sockInicio.connect(('localhost',int(PORTA)))
    sockInicio.send(str.encode('oi'))
    msg = sockInicio.recv(1024)
    print(str(msg, encoding = 'utf-8'))
    nosfilhos.append(sockInicio)

def finalizar():
    for i in nosfilhos:
        i.send(str.encode('exit'))
        time.sleep(1)
        i.close()
        print('finalizando o processo filho')


def ativar():
    n = input()
    nosfilhos[int(n)].send(str.encode('Ativar'))
    msg = nosfilhos[int(n)].recv(1024)
    print(str(msg, encoding = 'utf-8'))
    ativos.append(n)
    for i in ativos:
        atualizar(i)

def desativar(n):
    None
    ativos.drop(n)
    for i in ativos:
        atualizar(i)

def atualizar(n):
    None

def iniciaServidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
    sock.bind((HOST, PORT))

    sock.listen(5)

    sock.setblocking(False)

    entradas.append(sock)

    return sock

def aceitaConexao(sock):

    clisock, endr = sock.accept()

    conexoes[clisock] = endr 

    return clisock, endr

def atendeRequisicoes(clisock, endr):

    data = clisock.recv(1024)
        
    if (str(data, encoding = 'utf-8') == "Encerrar"):
        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()

    if (str(data, encoding = 'utf-8') == "Buscar"):
        quantidade = str(N)
        clisock.send(str.encode(quantidade))
        for i in portas:
            time.sleep(1)
            clisock.send(str.encode(str(i)))
        
    

def main():
    criarNos()
    
    sock = iniciaServidor()
    print("Pronto para receber conexoes...")
    while True:
        leitura, escrita, excecao = select.select(entradas, [], [])
        for pronto in leitura:
            if pronto == sock:
                clisock, endr = aceitaConexao(sock)
                print ('Conectado com: ', endr)
                clisock.setblocking(False)
                entradas.append(clisock)
            elif pronto == sys.stdin:
                cmd = input()
                if cmd == 'fim':
                    if not conexoes:
                        finalizar()
                        sock.close()
                        sys.exit()
                    else:
                        print("ha conexoes ativas")
                elif cmd == 'hist':
                    print(str(conexoes.values()))
                
                elif cmd == 'ativar':
                    ativar()

            else:
                atendeRequisicoes(pronto, conexoes[pronto])

main()
