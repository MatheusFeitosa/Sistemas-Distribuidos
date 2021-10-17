#imports
import socket
import select
import sys
import subprocess
import os
import time

HOST = '' 
PORT = 5788

N = 10

processos = []
ativos = []
portas = []

def criarNos():
    for i in range(N):
        PORTA = PORT + i + 1
        criarNo(i, N, PORTA)

#Referencia https://stackabuse.com/executing-shell-commands-with-python/
def criarNo(id, tamanho, PORTA):
    processo = subprocess.Popen(["python3", "no.py", str(id), str(PORTA), str(tamanho)])
    processos.append(processo)
    time.sleep(1)
    portas.append(PORTA)
    conectarInicio(PORTA)

def conectarInicio(PORTA):
    sockInicio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockInicio.connect(('localhost',int(PORTA)))
    sockInicio.send(str.encode('oi'))
    msg = sockInicio.recv(1024)
    print(str(msg, encoding = 'utf-8'))
    sockInicio.close()

def finalizar():
    for i in portas:
        sockFim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockFim.connect(('localhost', i))
        sockFim.send(str.encode('exit'))
        sockFim.close()


def ativar():
    None

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

	None

def main():
    criarNos()
    finalizar()

main()
