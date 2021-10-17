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
    for in range(tam):
        msg = sock.recv(1024)
        porta = str(msg, encoding = 'utf-8')
        portas.append(int(porta))
    return Nos

def buscarNo(Nos):
    tamanho = len(Nos)
    index = random.randint(0,tamanho-1)
    porta = Nos[index]

    return porta

def adicionarChaves(Nos, Chaves):
        
    for i in range(5):

        porta = buscarNo(Nos)
    
        sockNovo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sockNovo.connect(('localhost', porta))

        sockNovo.send(str.encode('Adicionar'))
        sockNovo.send(str.encode(Chaves))
        
        sockNovo.close()

        if not(resposta == 'Estou inativo'):
            return 0

    print('Tente mais tarde')


def removerChaves(Nos, chave):

    for i in range(5):

        porta = buscarNo(Nos)

        sockNovo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sockNovo.connect(('localhost', porta))

        sockNovo.send(str.encode('Remover'))
        sockNovo.send(str.encode(chave))

        sockNovo.close()

        if not(resposta == 'Estou inativo'):
            return 0

    print('Tente mais tarde')

def buscarValor(Nos, chave):
    for i in range(5):


        porta = buscarNo(Nos)

        sockNovo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sockNovo.connect(('localhost', porta))

        sockNovo.send(str.encode('Buscar'))
        sockNovo.send(str.encode(chave))
        valor = sockNovo.recv(1024)
        resposta = str(msg, encoding = 'utf-8'))
        sockNovo.close()
    
        if not(resposta == 'Estou inativo'):
            print(resposta)
            return 0

    print('Tente mais tarde')


def main():

    HOST = 'localhost'

    PORTA = 5788

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


