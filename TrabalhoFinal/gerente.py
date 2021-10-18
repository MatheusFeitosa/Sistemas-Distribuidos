#imports
import socket
import select
import sys
import subprocess
import os
import time
import math


HOST = '' 
PORT = 5500

entradas = [sys.stdin]
conexoes = {}

N = 8

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
    if not(n in ativos):
        ativos.append(n)
        for i in ativos:
            atualizar(i)

def desativar():
    n = input()
    nosfilhos[int(n)].send(str.encode('Desativar'))
    msg = nosfilhos[int(n)].recv(1024)
    print(str(msg, encoding = 'utf-8'))
    if(n in ativos):
        ativos.remove(n)
        for i in ativos:
            atualizar(i)

def atualizar(n):
    etapas = math.floor(math.log(N,2))
    for i in range(etapas):
        alcance = (2**i)
        aux = 0
        menor = N + 1
        menorGlobal = N + 1
        for j in ativos:
            num = int(j) - int(n)
            if( int(num%N) >= int(2**int(i))):
                menor = min(int(menor), int(num%N))
                aux = 1
            menorGlobal = min(int(menorGlobal), int(num%N))
        if(aux == 0):
            menor = menorGlobal
        sucessor = (int(menor) +int(n))%int(N)
        inicio = (int(n) + int(alcance))%int(N)
        ate = (int(n) + int(2**(i+1)) - 1)%int(N)
        nosfilhos[int(n)].send(str.encode('Atualizar'))
        msg = nosfilhos[int(n)].recv(1024)
        nosfilhos[int(n)].send(str.encode(str(inicio)))
        msg = nosfilhos[int(n)].recv(1024)
        nosfilhos[int(n)].send(str.encode(str(sucessor)))
        msg = nosfilhos[int(n)].recv(1024)
        nosfilhos[int(n)].send(str.encode(str(ate)))
        msg = nosfilhos[int(n)].recv(1024)
        nosfilhos[int(n)].send(str.encode(str(portas[int(sucessor)])))
        msg = nosfilhos[int(n)].recv(1024)

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
               
                elif cmd == 'desativar':
                    desativar()

            else:
                atendeRequisicoes(pronto, conexoes[pronto])

main()
