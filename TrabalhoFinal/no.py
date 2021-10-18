#imports
import socket
import select
import sys
import subprocess
import os
import time


entradas = []
conexoes = {}
estado = []
#Finger table
inicio = []
sucessor = {}
ate = {}


def iniciaServidor(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((HOST, int(PORT)))

    sock.listen(50)

    sock.setblocking(False)
    
    entradas.append(sock)

    return sock

def aceitaConexao(sock):

    clisock, endr = sock.accept()

    conexoes[clisock] = endr

    return clisock, endr


def atendeRequisicoes(clisock, endr):

    data = clisock.recv(1024)
    dataD = str(data, encoding = 'utf-8')        
    if (dataD == "oi"):
        clisock.send(str.encode(sys.argv[1]))

    if (dataD == "Ativar"):
        estado[0] = 1
        clisock.send(str.encode(str(estado[0])))
    

    if (dataD == "Buscar"):
        if(estado[0] == 0):
            clisock.send(str.encode('Estou inativo'))
        else:
            clisock.send(str.encode('Estou ativo'))
            time.sleep(1)
            msg = clisock.recv(1024)
            mensagem = str(msg, encoding = 'utf-8')
            clisock.send(str.encode(str(hash(mensagem))))
        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()

    if (dataD == "Remover"):
        if(estado[0] == 0):
            clisock.send(str.encode('Estou inativo'))
        else:
            clisock.send(str.encode('Estou ativo'))
            time.sleep(1)
            msg = clisock.recv(1024)
            mensagem = str(msg, encoding = 'utf-8')
            clisock.send(str.encode(str(hash(mensagem))))
        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()


    if (dataD == "Adicionar"):
        if(estado[0] == 0):
            clisock.send(str.encode('Estou inativo'))
        else:
            clisock.send(str.encode('Estou ativo'))
            time.sleep(1)
            msg = clisock.recv(1024)
            mensagem = str(msg, encoding = 'utf-8')
            partes = mensagem.split()
            clisock.send(str.encode(str(hash(partes[0]))))
        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()




    if dataD == "exit":
        return 1
    return 0



def main():
    id = int(sys.argv[1])
    PORT = int(sys.argv[2])
    tamanho = int(sys.argv[3])
    estado.append(0)
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
