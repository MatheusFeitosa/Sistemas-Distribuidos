#imports
import socket
import select
import sys
import subprocess
import os

#0 = inativo, 1 = ativo
estado = 0

entradas = [sys.stdin]
conexoes = {}

#Finger table
inicio = []
sucessor = {}
ate = {}


def iniciaServidor(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((HOST, int(PORT)))

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
        
    if (str(data, encoding = 'utf-8') == "oi"):
        clisock.send(str.encode(sys.argv[1]))
	
    del conexoes[clisock]
    entradas.remove(clisock)
    clisock.close()
    if str(data, encoding = 'utf-8') == "exit":
        return 1
    return 0



def main():
    id = int(sys.argv[1])
    PORT = int(sys.argv[2])
    tamanho = int(sys.argv[3])

    sock = iniciaServidor('',PORT)
    while True:
        leitura, escrita, excecao = select.select(entradas, [], [])
        for pronto in leitura:
            if(pronto == sock):
                clisock, endr = aceitaConexao(sock)
                clisock.setblocking(False)
                entradas.append(clisock)
            else:
                saida = atendeRequisicoes(pronto, conexoes[pronto])
                if(saida == 1):
                    sock.close()
                    sys.exit()

main()
