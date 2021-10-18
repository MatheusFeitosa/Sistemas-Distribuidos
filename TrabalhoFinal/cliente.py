#imports
import socket
import select
import sys
import subprocess
import os
import time
import random


def buscarNos(sock):
    sock.send(str.encode('Buscar'))
    msg = sock.recv(1024)
    tam = str(msg, encoding = 'utf-8')
    portas = []
    print(tam)
    tam = int(tam)
    for i in range(tam):
        msg = sock.recv(1024)
        porta = str(msg, encoding = 'utf-8')
        portas.append(int(porta))
    return portas

def buscarNo(Nos):
    tamanho = len(Nos)
    index = random.randint(0,tamanho-1)
    porta = Nos[index]

    return porta

def adicionarChaves(Nos, Chaves):
        
    for i in range(5):

        porta = buscarNo(Nos)
    
        sockNovo = socket.socket()
        print(porta)
        sockNovo.connect(('localhost', int(porta)))

        sockNovo.send(str.encode('Adicionar'))
        msg = sockNovo.recv(1024)
        resposta = str(msg, encoding = 'utf-8')

        if not(resposta == 'Estou inativo'):
            sockNovo.send(str.encode(Chaves))
            msg = sockNovo.recv(1024)
            resposta = str(msg, encoding = 'utf-8')
            print(resposta)
            sockNovo.close()
            return 0
        sockNovo.close()

    print('Tente mais tarde')


def removerChaves(Nos, chave):

    for i in range(5):

        porta = buscarNo(Nos)

        sockNovo = socket.socket()

        sockNovo.connect(('localhost', porta))

        sockNovo.send(str.encode('Remover'))
        msg = sockNovo.recv(1024)
        resposta = str(msg, encoding = 'utf-8')

        

        if not(resposta == 'Estou inativo'):
            sockNovo.send(str.encode(chave))
            msg = sockNovo.recv(1024)
            resposta = str(msg, encoding = 'utf-8')
            print(resposta)
            sockNovo.close()
            return 0

        sockNovo.close()

    print('Tente mais tarde')

def buscarValor(Nos, chave):
    for i in range(5):


        porta = buscarNo(Nos)

        sockNovo = socket.socket()

        sockNovo.connect(('localhost', porta))

        sockNovo.send(str.encode('Buscar'))
        msg = sockNovo.recv(1024)
        resposta = str(msg, encoding = 'utf-8')

        if not(resposta == 'Estou inativo'):
            sockNovo.send(str.encode(chave))
            msg = sockNovo.recv(1024)
            resposta = str(msg, encoding = 'utf-8')
            print(resposta)
            sockNovo.close()
            return 0
        sockNovo.close()

    print('Tente mais tarde')


def main():

    HOST = 'localhost'

    PORTA = 4988

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((HOST, PORTA))

    Nos = buscarNos(sock)

    while(1):
        print('O que deseja fazer?')
        action = input()
        
        if(str(action) == '1'):
            print('Escreva o par de chave e valor')
            valores = input()
            aux = valores.split()
            if(len(aux)>1):
                adicionarChaves(Nos, valores)
            else:
                print('Error!')

        if(str(action) == '2'):
            print('Escreva o valor da chave')
            valores = input()
            aux = valores.split()
            if(len(aux)==1):
                removerChaves(Nos, valores)
            else:
                print('Error!')

        if(str(action) == '3'):
            print('Escreva o valor da chave')
            valores = input()
            aux = valores.split()
            if(len(aux)==1):
                buscarValor(Nos, valores)
            else:
                print('Error!')

        if(str(action) == '4'):
            print('Encerrando')
            sock.send(str.encode('Encerrar'))
            sock.close()
            break

main()
